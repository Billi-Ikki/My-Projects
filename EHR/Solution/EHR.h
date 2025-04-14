#pragma once
#include"iotsensors.h"
class EHR
{
    Patient p;
    string id;
    string consultations;
    string prescriptions;
    string recommendations;
    string dietaryRestriction;
    string allergies;
    string regularMedication;
    string chronicHealthCondition;
public:
    EHR() {}
    EHR(Patient P);
    EHR(Patient P, string consultations, string prescriptions, string recommendations, string dietaryRestriction, string allergies, string regularMedication, string chronicHealthCondition);
    string getid()
    {
        return this->id;
    }
    void display();
    // Getter functions
    string getConsultations() const {
        return consultations;
    }

    string getPrescriptions() const {
        return prescriptions;
    }

    string getRecommendations() const {
        return recommendations;
    }

    string getDietaryRestriction() const {
        return dietaryRestriction;
    }

    string getAllergies() const {
        return allergies;
    }

    string getRegularMedication() const {
        return regularMedication;
    }
    string getChronicHealthCondition() const {
        return chronicHealthCondition;
    }
    // Setter functions
    void setConsultations(const string& value) {
        consultations = value;
    }

    void setPrescriptions(const string& value) {
        prescriptions = value;
    }

    void setRecommendations(const string& value) {
        recommendations = value;
    }

    void setDietaryRestriction(const string& value) {
        dietaryRestriction = value;
    }

    void setAllergies(const string& value) {
        allergies = value;
    }

    void setRegularMedication(const string& value) {
        regularMedication = value;
    }
    void setChronicHealthCondition(const string& value) {
        chronicHealthCondition = value;
    }
    void displayconsultation()
    {
        cout << endl << "Consultations : \n" << this->consultations << endl;
    }
};

