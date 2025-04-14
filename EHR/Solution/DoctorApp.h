#pragma once
#include"RMC.h"
class DoctorApp
{
private:
	Patient *p;
	iotsensors *i;
	RMC r;
	Doctor *d;
	Appointment* a;
	int patientindex;
	int docindex;
public:
	DoctorApp();
	DoctorApp(Patient *P, iotsensors *I, RMC R, Doctor *D,Appointment *A, int pi, int di , int iD, int iP);
	void working(int iD,int iP);
};

