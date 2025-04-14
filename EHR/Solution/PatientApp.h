#pragma once
#include"DoctorApp.h"
#include<fstream>
class PatientApp
{
private:
	RMC R;
	Patient *P;
	EHR *E;
	iotsensors *I;
	Appointment *A;
	Call *C;
	Doctor* D;
	int index;
public:
	PatientApp() {};
	PatientApp(Patient *p, EHR *e,iotsensors *i,Appointment *a,Call *c,Doctor *d);
	void Encryptions( int index, int doc_index, int iD, int iP);
	void P_Encryption(Patient P1);
	void E_Encrypt(EHR E,int);
	void I_Encrypt(iotsensors I,int);
	void C_Encrypt(Call C, int);
	void A_Encrypt(Appointment, int);
	void P_Decryption(Patient P1);
	void E_Decrypt(EHR E,int);
	void I_Decrypt(iotsensors I,int);
	void C_Decrypt(Call C, int);
	void A_Decrypt(Appointment, int);
	void working(int index, int doc_index, int iD, int iP, Patient* p, EHR* e, iotsensors* i, Appointment* a, Call* c, Doctor* d);
	void Decryptions(int index, int doc_index, int iD, int iP);
	RMC getRMC()
	{
		return this->R;
	}
};

