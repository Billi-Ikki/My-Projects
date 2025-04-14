#pragma once
#include"EHR.h"
class Call
{
private:
	Doctor D;
	string notes; 
	string recordstatus;
	int currentYear;
	int currentMonth;
	int currentDay;
public:
	Call();
	Call(Doctor D1);
	void working();
	void display();
    // Setters
    void setDoctor(const Doctor& doctor) {
        D = doctor;
    }

    void setNotes(const string& callNotes) {
        notes = callNotes;
    }

    void setRecordStatus(const string& status) {
        recordstatus = status;
    }

    void setCurrentYear(int year) {
        currentYear = year;
    }

    void setCurrentMonth(int month) {
        currentMonth = month;
    }

    void setCurrentDay(int day) {
        currentDay = day;
    }

    // Getters
    Doctor getDoctor() const {
        return D;
    }

    string getNotes() const {
        return notes;
    }

    string getRecordStatus() const {
        return recordstatus;
    }

    int getCurrentYear() const {
        return currentYear;
    }

    int getCurrentMonth() const {
        return currentMonth;
    }

    int getCurrentDay() const {
        return currentDay;
    }
};

