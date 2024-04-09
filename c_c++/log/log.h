/*
*@desc:		public.h
*@author:	me
*@date:		2023.1.26
*/

#ifndef LOG_H
#define LOG_H 1

#include<iostream>
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<time.h>
#include<sys/time.h>
#include<sys/syscall.h>
#include<fstream>
#include <string.h>
#include <thread>
#include <mutex>
#include <ctime>
#include <sys/stat.h>
#include <sys/types.h>

/*********************日志系统*******************************/

#define gettid()  syscall(SYS_gettid)

//extern std::ofstream fp;	//外部变量声明如此使用

enum LOG_LEVEL	//日志级别
{
	LOG_LEVEL_INFO,		//信息
	LOG_LEVEL_WARNING,	//警告
	LOG_LEVEL_ERROR		//错误
};


//__FILE__::获取当前文件名, __FUNCTION__::获取当前函数名, __LINE__::获取当前所在行数, __VA_ARGS__::可变参数列表
#define LOG_INFO(...)           Tools_Log::log(__FILE__,__FUNCTION__,__LINE__,LOG_LEVEL_INFO,__VA_ARGS__)
#define LOG_WARNING(...)        Tools_Log::log(__FILE__,__FUNCTION__,__LINE__,LOG_LEVEL_WARNING,__VA_ARGS__)
#define LOG_ERROR(...)          Tools_Log::log(__FILE__,__FUNCTION__,__LINE__,LOG_LEVEL_ERROR,__VA_ARGS__)

//日志系统
class Tools_Log
{
private:
	Tools_Log();
	~Tools_Log();
	Tools_Log(const Tools_Log &ciulog);
	const Tools_Log &operator = (const Tools_Log &ciulog);

	//Tools_Log() = delete;	//阻止构造
	//~Tools_Log() = delete;	//阻止析构
	//Tools_Log(const Tools_Log& rhs) = delete;	//阻止拷贝
	//Tools_Log& operator = (const Tools_Log& rhs) = delete;	//阻止赋值

private:
	bool		m_out_mode;	//日志写入文件还是控制台
	bool		m_mode;		//是否为多线程模式
	LOG_LEVEL	m_level;	//日志级别
	std::ofstream	m_fp;
	char			m_dir_path[200];

	static Tools_Log *		m_only;		//唯一单实列对象指针
	static pthread_mutex_t	m_mutex;	//互斥锁
public:
	static Tools_Log * g();	//获取单列实例
	//日志初始化,_mode输出到文件还是控制台,_is_thread是否为多线程,PCTSTR统一字符串
	void init(bool _mode, bool _is_thread);
	void set_dir_path(char * _path);
	void setlevel(LOG_LEVEL _level);	//修改日志级别
	bool log(const char * _file_name, const char* _fun_name, int _row, LOG_LEVEL _level, const char* _logstr,...);

};

extern "C"{
	// #define L_INFO(_str)	Tools_Log::g()->LOG_INFO(_str)
	// #define L_WARNING(_str)	Tools_Log::g()->LOG_INFO(_str)
	// #define L_ERROR(_str)	Tools_Log::g()->LOG_INFO(_str)

	void init(bool _out_mode, bool _is_thread){
		Tools_Log::g()->init(_out_mode, _is_thread);
		}
	void set_dir_path(char * _path){
		Tools_Log::g()->set_dir_path(_path);
	}
	void write_log(char * _file_name, char* _fun_name, int _row, LOG_LEVEL _level, char* _logstr){
		Tools_Log::g()->log(_file_name, _fun_name, _row, _level, _logstr);
	}
}

#endif
