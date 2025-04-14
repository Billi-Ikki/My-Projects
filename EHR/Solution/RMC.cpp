#include "RMC.h"
#include<fstream>
#include<iostream>
#include<string>
using namespace std;
RMC::RMC(){}
RMC::RMC(EHR* E1, iotsensors* I1, Appointment* A1, Call* C1)
{
	this->E = E1;
	this->I = I1;
	this->A = A1;
	this->C = C1;
}
void RMC::calldata(int index)
{
	int incrypt;
	string encrypt;
	int j = 0;
	encrypt = C[index].getNotes();
	while (encrypt[j] != '\0')
	{
		encrypt[j] -= '2';
		j++;
	}
	C[index].setNotes(encrypt);
	j = 0;
	encrypt = C[index].getRecordStatus();
	while (encrypt[j] != '\0')
	{
		encrypt[j] -= '2';
		j++;
	}
	C[index].setRecordStatus(encrypt);
	j = 0;
	incrypt = C[index].getCurrentDay();
	incrypt = incrypt >> 2;
	C[index].setCurrentDay(incrypt);

	incrypt = C[index].getCurrentMonth();
	incrypt = incrypt >> 2;
	C[index].setCurrentMonth(incrypt);

	incrypt = C[index].getCurrentYear();
	incrypt = incrypt >> 2;
	C[index].setCurrentYear(incrypt);
	Doctor D = C[index].getDoctor();
	cout << "Doctor Name  :  " << D.getName() << endl;
	cout << "Doctor ID    :  " << D.getID() << endl;
	cout << "Call Date    :  " << C[index].getCurrentDay() << "/" << C[index].getCurrentMonth() << "/" << C[index].getCurrentDay() << endl;
	cout << "Call Status  :  " << C[index].getRecordStatus() << endl;
	cout << "Notes        :  " << C[index].getNotes() << endl;
	 j = 0;
	encrypt = C[index].getNotes();
	while (encrypt[j] != '\0')
	{
		encrypt[j] += '2';
		j++;
	}
	C[index].setNotes(encrypt);
	j = 0;
	encrypt = C[index].getRecordStatus();
	while (encrypt[j] != '\0')
	{
		encrypt[j] += '2';
		j++;
	}
	C[index].setRecordStatus(encrypt);
	j = 0;
	incrypt = C[index].getCurrentDay();
	incrypt = incrypt << 2;
	C[index].setCurrentDay(incrypt);

	incrypt = C[index].getCurrentMonth();
	incrypt = incrypt << 2;
	C[index].setCurrentMonth(incrypt);

	incrypt = C[index].getCurrentYear();
	incrypt = incrypt << 2;
	C[index].setCurrentYear(incrypt);
}
void RMC::EHRdata(int i)
{
	// Removing Encryption
	string encryption;
	encryption = E[i].getAllergies();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setAllergies(encryption);

	encryption = E[i].getChronicHealthCondition();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setChronicHealthCondition(encryption);
	encryption = E[i].getConsultations();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setConsultations(encryption);
	encryption = E[i].getDietaryRestriction();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setDietaryRestriction(encryption);
	encryption = E[i].getPrescriptions();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setPrescriptions(encryption);


	encryption = E[i].getRecommendations();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setRecommendations(encryption);
	encryption = E[i].getRegularMedication();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setRegularMedication(encryption);
	cout << endl << "Consultation : " << E[i].getConsultations() << endl;
	cout << endl << "Prescriptions : " << E[i].getPrescriptions() << endl;
	cout << endl << "Recommendations : " << E[i].getRecommendations() << endl;
	cout << endl << "Dieatry Restrictions : " << E[i].getDietaryRestriction() << endl;
	cout << endl << "Allergies  : " << E[i].getAllergies() << endl;
	cout << endl << "Regular Medications : " << E[i].getRegularMedication() << endl;
	cout << endl << "Chronic Health Conditions : " << E[i].getChronicHealthCondition() << endl;
	// Again  Encryption
	encryption = E[i].getAllergies();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setAllergies(encryption);

	encryption = E[i].getChronicHealthCondition();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setChronicHealthCondition(encryption);
	encryption = E[i].getConsultations();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setConsultations(encryption);
	encryption = E[i].getDietaryRestriction();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setDietaryRestriction(encryption);
	encryption = E[i].getPrescriptions();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setPrescriptions(encryption);


	encryption = E[i].getRecommendations();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setRecommendations(encryption);
	encryption = E[i].getRegularMedication();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}

}
void RMC::EHRdataDA(int i)
{
	cout << endl << "Consultation : " << E[i].getConsultations() << endl;
	cout << endl << "Prescriptions : " << E[i].getPrescriptions() << endl;
	cout << endl << "Recommendations : " << E[i].getRecommendations() << endl;
	cout << endl << "Dieatry Restrictions : " << E[i].getDietaryRestriction() << endl;
	cout << endl << "Allergies  : " << E[i].getAllergies() << endl;
	cout << endl << "Regular Medications : " << E[i].getRegularMedication() << endl;
	cout << endl << "Chronic Health Conditions : " << E[i].getChronicHealthCondition() << endl;
}
void RMC::Appointmentdata(int i)
{
	// Removing Encryption
	string encrypt = A[i].getStatus();
	for (int j = 0; encrypt[j] != '\0'; j++)
	{
		encrypt[j] -= '2';
	}
	A[i].setStatus(encrypt);
	encrypt = A[i].getRTime();
	for (int j = 0; encrypt[j] != '\0'; j++)
	{
		encrypt[j] -= '2';
	}
	A[i].setRTime(encrypt);
	int incrypt;
	incrypt = A[i].getRHour();
	incrypt = incrypt >> 2;
	A[i].setRHour(incrypt);
	incrypt = A[i].getRMinute();
	incrypt = incrypt >> 2;
	A[i].setRMinute(incrypt);
	Patient P1 = A[i].getPatient();
	cout << "Patient Name : " << P1.getName() << endl;
	cout << "Patient ID   : " << P1.getID() << endl;
	cout << "Appointment Time : " << A[i].getRHour() << " : " << A[i].getRMinute() << "   " << A[i].getRTime() << endl;
	cout << "Status       : " << this->A[i].getStatus();
	// Again doing encryption
	 encrypt = A[i].getStatus();
	for (int j = 0; encrypt[j] != '\0'; j++)
	{
		encrypt[j] += '2';
	}
	A[i].setStatus(encrypt);
	encrypt = A[i].getRTime();
	for (int j = 0; encrypt[j] != '\0'; j++)
	{
		encrypt[j] += '2';
	}
	A[i].setRTime(encrypt);
	incrypt = A[i].getRHour();
	incrypt = incrypt << 2;
	A[i].setRHour(incrypt);
	incrypt = A[i].getRMinute();
	incrypt = incrypt << 2;
	A[i].setRMinute(incrypt);
}
void RMC::IOTdata(int i)
{
	//Removing Encryption
	int size = 0;
	int encryp = 0;
	encryp = I[i].getDay();
	encryp = encryp >> 2;
	I[i].setDay(encryp);
	encryp = I[i].getMonth();
	encryp = encryp >> 2;
	I[i].setMonth(encryp);
	encryp = I[i].getYear();
	encryp = encryp >> 2;
	I[i].setYear(encryp);
	size = I[i].getSize();
	int* encryption;
	encryption = new int[size];
	for (int j = 0; j < size; j++)
	{
		encryption = I[i].getBmi();
		encryption[j] = encryption[j] >> 2;
		I[i].setBmi(encryption);
		encryption = I[i].getOxygenSaturation();
		encryption[j] = encryption[j] >> 2;
		I[i].setOxygenSaturation(encryption);
		encryption = I[i].getPulse();
		encryption[j] = encryption[j] >> 2;
		I[i].setPulse(encryption);
		encryption = I[i].getBloodPressure();
		encryption[j] = encryption[j] >> 2;
		I[i].setBloodPressure(encryption);
		encryption = I[i].getHandTremor();
		encryption[j] = encryption[j] >> 2;
		I[i].setHandTremor(encryption);
		encryption = I[i].getGeneralMovement();
		encryption[j] = encryption[j] >> 2;
		I[i].setGeneralMovement(encryption);
	}
	I[i].Displayall();
		//int Day = 1;
		//int Month = 2;
		//int Year = 2023;
		//Patient P = I[i].getPatient();
		////int size = I[i].getSize();
		//cout << "Patient name : " << P.getName() << endl;
		//cout << "Patient Id   : " << P.getID() << endl;
		//cout << "Sr#\tDate\t\tOxygen saturation\tPulse\t\tBMI\t   Blood Pressure\tHand Termor\tGeneral Movement" << endl;
		//for (int i = 0; i < size; i++)
		//{
		//	cout << i << "\t" << Day << "/" << Month << "/" << Year << "\t" << I[i].getOxygenSaturation(i) << "\t\t\t" << I[i].getPulse(i) << "\t\t"
		//		<< I[i].getBmi(i)<< "\t\t" << I[i].getBloodPressure(i) << "\t\t" << I[i].getHandTremor(i) <<
		//		"\t\t" << I[i].getGeneralMovement(i) << "\t\t\n";

		//	Day++;
		//	if (Day % 31 == 0)
		//	{
		//		Day = 1;
		//		Month++;
		//		if (Month % 13 == 0)
		//		{
		//			Month == 1;
		//			Year++;
		//		}
		//	}
		//}
	//Again Doing Encryption
	encryp = I[i].getDay();
	encryp = encryp << 2;
	I[i].setDay(encryp);
	encryp = I[i].getMonth();
	encryp = encryp << 2;
	I[i].setMonth(encryp);
	encryp = I[i].getYear();
	encryp = encryp << 2;
	I[i].setYear(encryp);
	size = I[i].getSize();
	for (int j = 0; j < size; j++)
	{
		encryption = I[i].getBmi();
		encryption[j] = encryption[j] << 2;
		I[i].setBmi(encryption);
		encryption = I[i].getOxygenSaturation();
		encryption[j] = encryption[j] << 2;
		I[i].setOxygenSaturation(encryption);
		encryption = I[i].getPulse();
		encryption[j] = encryption[j] << 2;
		I[i].setPulse(encryption);
		encryption = I[i].getBloodPressure();
		encryption[j] = encryption[j] << 2;
		I[i].setBloodPressure(encryption);
		encryption = I[i].getHandTremor();
		encryption[j] = encryption[j] << 2;
		I[i].setHandTremor(encryption);
		encryption = I[i].getGeneralMovement();
		encryption[j] = encryption[j] << 2;
		I[i].setGeneralMovement(encryption);
	}
}
void RMC::consultationsdata(int i)
{
	
	string consultationsdata;
	consultationsdata = E[i].getConsultations();
	//for (int i = 0; consultationsdata[i] != '\0'; i++)
	//{
	//	consultationsdata[i] -= '2';
	//}
	cout << "Consultations : " << consultationsdata << endl;
	//
	//consultationsdata = E[i].getConsultations();
	//for (int i = 0; consultationsdata[i] != '\0'; i++)
	//{
	//	consultationsdata[i] += '2';
	//}
}
void RMC::reterivedatacall(int index)
{
	RMC temp;
	ifstream myFile("Cloud.dat", ios::binary);
	while (myFile.read((char*)&temp, sizeof(temp)))
	{
		temp.calldata(index);
	}
	myFile.close();
}
void RMC::reterivedataEhr(int index)
{
	RMC temp;
	ifstream myFile("Cloud.dat", ios::binary);
	while (myFile.read((char*)&temp, sizeof(temp)))
	{
		temp.EHRdata(index);
	}
	myFile.close();
}
void RMC::reteriveAppointment(int index)
{
	RMC temp;
	ifstream myFile("Cloud.dat", ios::binary);
	while (myFile.read((char*)&temp, sizeof(temp)))
	{
		temp.Appointmentdata(index);
	}
	myFile.close();
}
void RMC::reteriveiotData(int index)
{
	RMC temp;
	ifstream myFile("Cloud.dat", ios::binary);
	while (myFile.read((char*)&temp, sizeof(temp)))
	{
		temp.IOTdata(index);
	}
	myFile.close();
}
void reteriveconsultations(int index)
{
	RMC temp;
	ifstream myFile("Cloud.dat", ios::binary);
	while (myFile.read((char*)&temp, sizeof(temp)))
	{
		temp.consultationsdata(index);
	}
	myFile.close();
}
void RMC::ehr(int id)
{
	string add;
	int choice2 = 0;
	cout << "1 : Add Consultations \n";
	cout << "2 : Add Allergies \n";
	cout << "3 : Add Dietry Restrictions\n";
	cin >> choice2;
	if (choice2 == 1)
	{
		cout << "Enter Consultations you want to add  : " << endl;
		cin.ignore();
		getline(cin, add);
		add += E[id].getConsultations();
		E[id].setConsultations(add);
		cout << "Added Successfully" << endl;
	}
	else if (choice2 == 2)
	{
		cout << "Enter Allergies you want to add  : " << endl;
		cin.ignore();
		getline(cin, add);
		add += E[id].getAllergies();
		E[id].setAllergies(add);
		cout << "Added Successfully" << endl;
	}
	else if (choice2 == 3)
	{

		cout << "Enter Dietry restrictions you want to add  : " << endl;
		cin.ignore();
		getline(cin, add);
		add += E[id].getDietaryRestriction();
		E[id].setDietaryRestriction(add);
		cout << "Added Successfully" << endl;
	}
	else
	{
		cout << "\nINVALID CHOICE\n";
	}
}
void RMC::updateObject(int pid, string add, int choice)
{
	int i;
	if (choice == 1)
	{
		E[pid].setConsultations(add);
	}
	else if (choice == 2)
	{
		E[pid].setPrescriptions(add);
	}
	else if (choice == 3)
	{
		E[pid].setRecommendations(add);
	}
	else if (choice == 4)
	{
		E[pid].setDietaryRestriction(add);
	}
	else if (choice == 5)
	{
		E[pid].setAllergies(add);
	}
	else if (choice == 6)
	{
		E[pid].setRegularMedication(add);
	}
	else
	{
		E[pid].setChronicHealthCondition(add);
	}
	//fstream myFile("Cloud.dat", ios::in | ios::out | ios::binary);
	//while (myFile.read((char*)&temp, sizeof(temp))) {
	//	if (temp.getid() == id) {
	//		strcpy(str, add.c_str());
	//		double current = myFile.tellg();
	//		double oneblock = sizeof(temp);
	//		myFile.seekg(current - oneblock);
	//		myFile.write((char*)&temp, sizeof(temp));
	//		myFile.close();
	//	}
	//}
}