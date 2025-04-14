#include "iotsensors.h"
iotsensors::iotsensors()
{
    this->day = 7;
    this->month = 2;
    this->year = 2023;
    time_t currentTime = time(nullptr);
    tm* localTime = localtime(&currentTime);
    int currentYear = localTime->tm_year + 1900;
    int currentMonth = localTime->tm_mon + 1;
    int currentDay = localTime->tm_mday;
    this->year = currentYear - this->year;
    int totaldays = 0;
    if (currentMonth < this->month) // checking conditions
    {
        this->year = this->year - 1;
        this->month = (currentMonth + 12) - this->month;
    }
    else
    {
        this->month = currentMonth - this->month;
    }
    if (currentDay < this->day)
    {
        this->month = this->month - 1;
        this->day = (currentDay + 30) - this->day;
    }
    else
        this->day = currentDay - this->day;
    totaldays = this->year * 365 + this->month * 30 + this->day;
    this->size = totaldays;
    OxygenSaturation();
    Pulse();
    BMI();
    BloodPressure();
    HandTremor();
    GeneralMovement();
    FallDetection();
}
iotsensors::iotsensors(Patient P1)
{
    this->P = P1;
    this->day = 7;
    this->month = 2;
    this->year = 2023;
    time_t currentTime = time(nullptr);
    tm* localTime = localtime(&currentTime);
    int currentYear = localTime->tm_year + 1900;
    int currentMonth = localTime->tm_mon + 1;
    int currentDay = localTime->tm_mday;
    this->year = currentYear - this->year;
    int totaldays = 0;
    if (currentMonth < this->month) // checking conditions
    {
        this->year = this->year - 1;
        this->month = (currentMonth + 12) - this->month;
    }
    else
    {
        this->month = currentMonth - this->month;
    }
    if (currentDay < this->day)
    {
        this->month = this->month - 1;
        this->day = (currentDay + 30) - this->day;
    }
    else
        this->day = currentDay - this->day;
    totaldays = this->year * 365 + this->month * 30 + this->day;
    this->size = totaldays;
    OxygenSaturation();
    Pulse();
    BMI();
    BloodPressure();
    HandTremor();
    GeneralMovement();
    FallDetection();
}
void iotsensors::Displayall()
{
    int Day = 1;
    int Month = 2;
    int Year = 2023;
    cout << "Patient name : " << this->P.getName() << endl;
    cout << "Patient Id   : " << this->P.getID() << endl;
    cout << "Sr#\tDate\t\tOxygen saturation\tPulse\t\tBMI\t   Blood Pressure\tHand Termor\tGeneral Movement" << endl;
    for (int i = 0; i < this->size; i++)
    {
        cout << i << "\t" << Day << "/" << Month << "/" << Year << "\t" << oxygensaturation[i] << "\t\t\t" << pulse[i] << "\t\t"
            << B_M_I[i] << "\t\t" << BP[i] << "\t\t" << handtermor[i] <<
            "\t\t" << generalmovement[i] << "\t\t\n";

        Day++;
        if (Day % 31 == 0)
        {
            Day = 1;
            Month++;
            if (Month % 13 == 0)
            {
                Month == 1;
                Year++;
            }
        }
    }
}
