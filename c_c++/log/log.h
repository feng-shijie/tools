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

/*********************日志系统*******************************/

#define LOG_FILE "log"
#define gettid()  syscall(SYS_gettid)

//extern std::ofstream fp;	//外部变量声明如此使用

enum LOG_LEVEL	//日志级别
{
	LOG_LEVEL_INFO,		//信息
	LOG_LEVEL_WARNING,	//警告
	LOG_LEVEL_ERROR		//错误
};


//__FILE__::获取当前文件名, __FUNCTION__::获取当前函数名, __LINE__::获取当前所在行数, __VA_ARGS__::可变参数列表
#define LOG_INFO(...)           CIULOG::log(__FILE__,__FUNCTION__,__LINE__,LOG_LEVEL_INFO,__VA_ARGS__)
#define LOG_WARNING(...)        CIULOG::log(__FILE__,__FUNCTION__,__LINE__,LOG_LEVEL_WARNING,__VA_ARGS__)
#define LOG_ERROR(...)          CIULOG::log(__FILE__,__FUNCTION__,__LINE__,LOG_LEVEL_ERROR,__VA_ARGS__)

//日志系统
class CIULOG
{
private:
	CIULOG();
	~CIULOG();
	CIULOG(const CIULOG &ciulog);
	const CIULOG &operator = (const CIULOG &ciulog);

	//CIULOG() = delete;	//阻止构造
	//~CIULOG() = delete;	//阻止析构
	//CIULOG(const CIULOG& rhs) = delete;	//阻止拷贝
	//CIULOG& operator = (const CIULOG& rhs) = delete;	//阻止赋值

private:
	bool		m_out_mode;	//日志写入文件还是控制台
	bool		m_mode;		//是否为多线程模式
	LOG_LEVEL	m_level;	//日志级别
	std::ofstream	m_fp;

	static CIULOG *			m_only;		//唯一单实列对象指针
	static pthread_mutex_t	m_mutex;	//互斥锁
public:
	static CIULOG * g();	//获取单列实例
	//日志初始化,_mode输出到文件还是控制台,_is_thread是否为多线程,PCTSTR统一字符串
	void init(bool _mode, bool _is_thread);
	void setlevel(LOG_LEVEL _level);	//修改日志级别
	bool log(const char * _file_name, const char* _fun_name, int _row, LOG_LEVEL _level, const char* _logstr,...);

};

#endif
