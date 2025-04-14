#include"EHR.h"
EHR::EHR(Patient P)
{
    p = P;
    id = P.getID();
    consultations = "Patient has  Diadetes. ";
    prescriptions = "Metformin Take 500mg orally twice daily with meal Insulin";
    recommendations = "Check blood glucose levels before meals and at bedtime";
    dietaryRestriction = "Limit sugary and processed foods";
    allergies = "basic skin allergy";
    regularMedication = "Sitagliptin Take 100mg orally once daily in the morning.";
    chronicHealthCondition = "High blood sugar levels.Use Insulin, a hormone responsible for regulating blood glucose levels.";
}
EHR::EHR(Patient P, string consultations, string prescriptions, string recommendations, string dietaryRestriction, string allergies, string regularMedication, string chronicHealthCondition)
{
    this->p = P;
    this->consultations = consultations;
    this->prescriptions = prescriptions;
    this->recommendations = recommendations;
    this->dietaryRestriction = dietaryRestriction;
    this->allergies = allergies;
    this->regularMedication = regularMedication;
    this->chronicHealthCondition = chronicHealthCondition;
}
void EHR::display()
{
    cout << endl << "Consultation : " << consultations << endl;
    cout << endl << "Prescriptions : " << prescriptions << endl;
    cout << endl << "Recommendations : " << recommendations << endl;
    cout << endl << "Dieatry Restrictions : " << dietaryRestriction << endl;
    cout << endl << "Allergies  : " << allergies << endl;
    cout << endl << "Regular Medications : " << regularMedication << endl;
    cout << endl << "Chronic Health Conditions : " << chronicHealthCondition << endl;
}