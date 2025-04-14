#pragma once
#include"Appointment.h"
class RMC
{
private:
	EHR *E;
	iotsensors *I;
	Appointment *A;
	Call *C;
public:
	RMC();
	RMC(EHR* E1, iotsensors* I1, Appointment* A1, Call* C1);
    void calldata(int index);
    void Appointmentdata(int i);
    void EHRdata(int i);
    void EHRdataDA(int i);
    void IOTdata(int i);
    void consultationsdata(int i);
    void reterivedatacall(int index);
    void reterivedataEhr(int index);
    void reteriveAppointment(int index);
    void reteriveiotData(int index);
    void reteriveconsultations(int index);
    void ehr(int index);
    void updateObject(int, string, int);
    //Setters
    void setEHR(EHR* ehr) {
        E = ehr;
    }

    void setIotSensors(iotsensors* sensors) {
        I = sensors;
    }

    void setAppointment(Appointment* appointment) {
        A = appointment;
    }

    void setCall(Call* call) {
        C = call;
    }

    // Getters
    EHR getEHR(int index) const {
        return E[index];
    }
    iotsensors getIotSensors(int index) const {
        return I[index];
    }
    Appointment getAppointment(int index) const {
        return A[index];
    }
    Call getCall(int index) const {
        return C[index];
    }
};

