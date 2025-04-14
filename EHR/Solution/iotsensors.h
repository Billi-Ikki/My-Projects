#pragma once
#include"Patient.h"
#pragma warning(disable : 4996)
class iotsensors
{
private:
    Patient P;
    int day;
    int month;
    int year;
    int size;
    int* B_M_I;
    int* oxygensaturation;
    int* pulse;
    int* BP;
    int* handtermor;
    int* generalmovement;
    bool* falldetect;
public:

    iotsensors();
    iotsensors(Patient P1);
    void Displayall();

    Patient getPatient() const {
        return P;
    }
    int getDay() const {
        return day;
    }
    void setDay(int value) {
        day = value;
    }
    int getMonth() const {
        return month;
    }
    void setMonth(int value) {
        month = value;
    }
    
    int getYear() const {
        return year;
    }

    void setYear(int value) {
        year = value;
    }
    int getSize() const {
        return size;
    }

    void setSize(int value) {
        size = value;
    }

    int* getBmi() const {
        return B_M_I;
    }

    void setBmi(int* value) {
        B_M_I = value;
    }

    int* getOxygenSaturation() const {
        return oxygensaturation;
    }

    void setOxygenSaturation(int* value) {
        oxygensaturation = value;
    }
    int* getPulse() const {
        return pulse;
    }

    void setPulse(int* value) {
        pulse = value;
    }

    int* getBloodPressure() const {
        return BP;
    }

    void setBloodPressure(int* value) {
        BP = value;
    }

    int* getHandTremor() const {
        return handtermor;
    }

    void setHandTremor(int* value) {
        handtermor = value;
    }

    int* getGeneralMovement() const {
        return generalmovement;
    }

    void setGeneralMovement(int* value) {
        generalmovement = value;
    }
    
    double generateRandomValue(double minValue, double maxValue)
    {
        double randomValue = ((double)rand() / RAND_MAX) * (maxValue - minValue) + minValue;
        return randomValue;
    }

    double OxygenSaturation()
    {
        double minValue = 90.0;   // Minimum oxygen saturation value
        double maxValue = 100.0;  // Maximum oxygen saturation value
        this->oxygensaturation = new int[size];
        for (int i = 0; i < this->size; i++)
        {
            oxygensaturation[i] = generateRandomValue(minValue, maxValue);
        }
        return generateRandomValue(minValue, maxValue);
    }
    double Pulse()
    {
        double minValue = 60.0;   // Minimum pulse value
        double maxValue = 120.0;  // Maximum pulse value
        this->pulse = new int[size];
        for (int i = 0; i < this->size; i++)
        {
            pulse[i] = generateRandomValue(minValue, maxValue);
        }
        return generateRandomValue(minValue, maxValue);
    }
    double BMI()
    {

        double minValue = 18.5;   // Minimum BMI value
        double maxValue = 30.0;   // Maximum BMI value
        this->B_M_I = new int[size];
        for (int i = 0; i < this->size; i++)
        {
            B_M_I[i] = generateRandomValue(minValue, maxValue);
        }
        return generateRandomValue(minValue, maxValue);

    }
    double BloodPressure()
    {
        double minValue = 90.0;   // Minimum blood pressure value
        double maxValue = 140.0;  // Maximum blood pressure value
        this->BP = new int[size];
        for (int i = 0; i < this->size; i++)
        {
            BP[i] = generateRandomValue(minValue, maxValue);
        }
        return generateRandomValue(minValue, maxValue);
    }
    double HandTremor()
    {
        double minValue = 0.0;    // Minimum hand tremor value
        double maxValue = 10.0;   // Maximum hand tremor value
        this->handtermor = new int[size];
        for (int i = 0; i < this->size; i++)
        {
            handtermor[i] = generateRandomValue(minValue, maxValue);
        }
        return generateRandomValue(minValue, maxValue);
    }
    double GeneralMovement()
    {
        double minValue = 0.0;    // Minimum general movement value
        double maxValue = 100.0;  // Maximum general movement value
        this->generalmovement = new int[size];
        for (int i = 0; i < this->size; i++)
        {
            generalmovement[i] = generateRandomValue(minValue, maxValue);
        }
        return generateRandomValue(minValue, maxValue);
    }
    bool   FallDetection()
    {
        // 80% chance of not detecting a fall (false)
        // 20% chance of detecting a fall (true)
        this->falldetect = new bool[size];
        for (int i = 0; i < this->size; i++)
        {
            falldetect[i] = (rand() % 100) < 20;
        }
        return (rand() % 2);
    }
    void setPatient(Patient P1)
    {
        this->P = P1;
    }


};

