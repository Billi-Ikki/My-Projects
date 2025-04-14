#include "Appointment.h"
Appointment::Appointment(Doctor D1)
{

    //this->time = new string[2];
    this->status = "Pending";
    this->P.setName("Bilal");
    this->P.setID("1");
    this->rhour = 12;
    this->rtime = "PM";
    this->rmint = 30;
    this->D = D1;
    for (int i = 0; i < 10; i++)
    {
        hour[i] = rand() % 12;
        minutes[i] = rand() % 60;
        if (rand() % 2 == 0)
        {
            time[i] = "AM";
        }
        else
        {
            time[i] = "PM";
        }
    }
}
void Appointment::appointmentlist(Patient P)
{
    this->P = P;
    int appchoice = 0;
    for (int i = 0; i < 10; i++)
    {
        cout << i + 1 << " :\t" << hour[i] << " : " << minutes[i] << "\t" << time[i] << endl;
    }
    cout << "Enter Your choice : ";
    cin >> appchoice;
    appchoice -= 1;
    this->rhour = hour[appchoice];
    this->rmint = minutes[appchoice];
    this->rtime = time[appchoice];
    system("cls");
    cout << "\t\t\t\t\tAppointment request sended Successfully " << endl;
}
void Appointment::appointmentrequests()
{
    cout << "Patient Name : " << P.getName() << endl;
    cout << "Patient ID   : " << P.getID() << endl;
    cout << "Appointment Time : " << rhour << " : " << rmint << "   " << rtime << endl;
    cout << "Status       : " << this->status << endl;
}
