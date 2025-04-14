#pragma once
#include<iostream>
#include"Call.h"
using namespace std;
class Appointment
{
	string status;
    int hour[10];
    int minutes[10];
    string time[10];
    int rhour;
    int rmint;
    string rtime;
    Doctor D;
    Patient P;
public:
    Appointment()
    {
        status = "Pending";
    }
    Appointment(Doctor D);
    void appointmentlist(Patient P);
    void appointmentrequests();
    // Setters
    void setStatus(const string& appointmentStatus) {
        status = appointmentStatus;
    }

    void setRHour(int hour) {
        rhour = hour;
    }

    void setRMinute(int minute) {
        rmint = minute;
    }

    void setRTime(const string& time) {
        rtime = time;
    }

    // Getters
    string getStatus() const {
        return status;
    }

    int getRHour() const {
        return rhour;
    }

    int getRMinute() const {
        return rmint;
    }

    string getRTime() const {
        return rtime;
    }
    Patient getPatient()
    {
        return this->P;
    }
};

