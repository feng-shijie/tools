#include "log.h"

//代码一运行就初始化创建实例,本身就线程安全
Tools_Log* Tools_Log::m_only 	  = new(std::nothrow)Tools_Log();
pthread_mutex_t	Tools_Log::m_mutex;

Tools_Log::Tools_Log(){
	m_mode 		= false;			//默认为单线程不需要使用互斥锁
	m_out_mode 	= true;				//默认输入到日志文件内
	m_level 	= LOG_LEVEL_INFO;	//默认日志级别为信息输出
	memcpy(m_dir_path, "log_info", strlen("log_info"));
}

Tools_Log::~Tools_Log()
{
	if(m_only){
		delete m_only;
		m_only = nullptr;
	}
}

Tools_Log * Tools_Log::g(){
	static std::mutex mu_lock;

	if(m_only == nullptr){
		mu_lock.lock();
		if(m_only == nullptr)	m_only = new Tools_Log();
		mu_lock.unlock();
	}
	return m_only;
}

//日志初始化,_mode输出到文件还是控制台,_is_thread是否为多线程,PCTSTR统一字符串
void Tools_Log::init(bool _mode, bool _is_thread)
{
	m_out_mode 	= _mode;
	m_mode		= _is_thread;

	//如果有同名的文件也是返回0的
	if(access(m_dir_path, 0) != 0){
		if(mkdir(m_dir_path, ACCESSPERMS) != 0){
			std::cout << "created dir fail" << std::endl;
			return;
		}
	}
	if(_is_thread){
		if(pthread_mutex_init(&m_mutex,0) !=0)	//初始化互斥锁
			LOG_ERROR("mutex init error");
	}

}

void Tools_Log::set_dir_path(char * _path){
	memcpy(m_dir_path, _path, strlen(_path));
}

void Tools_Log::setlevel(LOG_LEVEL _level)  //设置日志级别
{
	m_level = _level;
}

bool Tools_Log::log(const char * _file_name, const char* _fun_name, int _row, LOG_LEVEL _level, const char * _logstr,...)
{
	//判断是否为多线程
	if(m_mode){
		if(pthread_mutex_lock(&m_mutex) != 0){	//加锁
			m_mode = false;
			LOG_ERROR("lock error");
			return false;
		}
	}

	char levelname[10];
	memset(levelname, 0, sizeof(levelname));
	
	if(		_level == LOG_LEVEL_INFO	)	strcpy(levelname, "INFO");
	else if(_level == LOG_LEVEL_WARNING )	strcpy(levelname, "WARNING");
	else if(_level == LOG_LEVEL_ERROR	)	strcpy(levelname, "ERROR");

	char time_string[40];
	time_t t_now = time(0);			//获取时间戳
	tm * ltm = localtime(&t_now);	//转为tm结构体
	strftime(time_string,sizeof(time_string), "%H:%M:%S", ltm);

	if(m_out_mode){
re_open:
		char c_name[250], c_head[300];
		memset(c_head, 0, sizeof(c_head));
		memset(c_name, 0, sizeof(c_name));

		static int i_val = 0;
		sprintf(c_name,"%s/log_%d_%d_%d.txt", m_dir_path, ltm->tm_mon + 1, ltm->tm_mday, i_val);
		sprintf(c_head,"[%s][%s][%s][%s(): %d]::",time_string, levelname,_file_name, _fun_name, _row);

		m_fp.open(c_name, std::ios::out | std::ios::app);
		if(!m_fp.is_open()){
			std::cout << "file:: " << c_name << " open fail\n";
			return false;
		}

		//文件大小不超过2MB
		std::streampos f_size = m_fp.tellp();
		if(f_size > 1024 * 1000 * 2){
			m_fp.close();
			++i_val;
			goto re_open;
		}

		m_fp << c_head << _logstr << '\n';
		m_fp.close();
	}
	else{
		printf("[%s][%s][PID:%u][TID:%u][%s][%s: %d]::%s\n",time_string,levelname,
		(unsigned int)getpid(),(unsigned int)gettid(), _file_name, _fun_name, _row, _logstr);
	}

	if(m_mode){
		if(pthread_mutex_unlock(&m_mutex) != 0){
			m_mode = false;
			LOG_ERROR("unlock error");
			return false;
		}
	}
	return true;
}