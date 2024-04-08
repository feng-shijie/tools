#include "log.h"

//代码一运行就初始化创建实例,本身就线程安全
CIULOG* CIULOG::m_only 	  = new(std::nothrow)CIULOG();
pthread_mutex_t	CIULOG::m_mutex;

CIULOG::CIULOG(){
	m_fp		= new std::ofstream();
	m_mode 		= false;			//默认为单线程不需要使用互斥锁
	m_out_mode 	= true;				//默认输入到日志文件内
	m_level 	= LOG_LEVEL_INFO;	//默认日志级别为信息输出
}

CIULOG::~CIULOG()
{
	if(m_only){
		delete m_only;
		m_only = nullptr;
	}
	if(m_fp){
		delete m_fp;
		m_fp = nullptr;
	}
}

CIULOG * CIULOG::g(){
	static std::mutex mu_lock;

	if(m_only == nullptr){
		mu_lock.lock();
		if(m_only == nullptr)	m_only = new CIULOG();
		mu_lock.unlock();
	}
	return m_only;
}

//日志初始化,_mode输出到文件还是控制台,_is_thread是否为多线程,PCTSTR统一字符串
void CIULOG::init(bool _mode, bool _is_thread)
{
	m_out_mode 	= _mode;
	m_mode		= _is_thread;

	if(_is_thread){
		if(pthread_mutex_init(&m_mutex,0) !=0)	//初始化互斥锁
			LOG_ERROR("mutex init error");
	}

}
void CIULOG::setlevel(LOG_LEVEL _level)  //设置日志级别
{
	m_level = _level;
}

bool CIULOG::log(const char * _file_name, const char* _fun_name, int _row, LOG_LEVEL _level, const char * _logstr,...)
{
	//判断是否为多线程
	if(m_mode){
		if(pthread_mutex_lock(&m_mutex) != 0){	//加锁
			m_mode = false;
			LOG_ERROR("lock error");
			return false;
		}
	}

	char str[2048],levelname[10];
	memset(str,0,sizeof(str));
	memset(levelname,0,sizeof(levelname));
	
	if(		_level == LOG_LEVEL_INFO	)	strcpy(levelname, "INFO");
	else if(_level == LOG_LEVEL_WARNING )	strcpy(levelname, "WARNING");
	else if(_level == LOG_LEVEL_ERROR	)	strcpy(levelname, "ERROR");

	char time_string[40];
	time_t t_now = time(0);			//获取时间戳
	tm * ltm = localtime(&t_now);	//转为tm结构体
	strftime(time_string,sizeof(time_string), "%H:%M:%S", ltm);

	if(m_out_mode){
		char c_name[10];
		sprintf(c_name,"%s_%d", LOG_FILE, ltm->tm_mday);
		sprintf(str,"[%s][%s][%s][%s(): %d]::%s\n",time_string, levelname,_file_name, _fun_name, _row, _logstr);
		//每次写日志要打开文件
		m_fp->open(c_name, std::ios::out | std::ios::app);
		if(!m_fp->is_open()){
			std::cout << "file:: " << c_name << " open fail\n";
			return false;
		}
		*m_fp << str;
		m_fp->close();	//写完后关闭文件
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