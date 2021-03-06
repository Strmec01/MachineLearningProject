# api_sequences_malware_datasets

##  Dynamic malware analysis benchmarks

New datasets for dynamic malware classification are built based on the hashcodes of malware files, API calls from PEFile library in Python, and the malware type from the VirusTotal API, presented in CSV format. One of these datasets contains 9,795 samples obtained and compiled from VirusSamples, and the other contains 14,616 samples from VirusShare. 

VirusSample dataset includes the malware families of Adware, Agent, Backdoor, Trojan, Virus, Worms, Downloader, Spyware, Ransomware, Riskware, Dropper, Crypt, Keylogger. 

VirusShare dataset includes families of Adware, Agent, Backdoor, Downloader, Ransomware, Riskware, Trojan, Virus, Worms, Undefined, Spyware, Dropper, Crypt, Keylogger, Rootkit. 

VirusSample: Machine learning algorithms deal poorly with class imbalance, so we rebalanced datasets by undersampling the over-represented classes to a maximum of 300 samples per class and imposing a hard lower threshold on under-represented families, considering only those categories represented by at least 80 samples. The balanced dataset consists of 1,324 malware samples belonging to 6 families: Adware, Agent, Backdoor, Trojan, Virus, Worms.

Metric For Balanced Version of VirusSample Dataset  | HGB | RF | SVM | XGB
-------------     | ------------- | ------------- | ------------- | -------------
Accuracy          | 0.90  	  |0.82		  |0.91		  |0.90
Macro avg. F1       | 0.89	  |0.83		  |0.91		  |0.90
Weighted avg. F1     | 0.89	  |0.81		  |0.91		  |0.90




Metric For Imbalanced Version of VirusSample Dataset  | HGB | RF | SVM | XGB
-------------     | ------------- | ------------- | ------------- | -------------
Accuracy          | 0.93  	  |0.84		  |0.94	  |0.90
Macro avg. F1       |0.73	  |0.64		  |0.75		  |0.75
Weighted avg. F1     | 0.93	  |0.83		  |0.94		  |0.94				
				

VirusShare: Again, we rebalanced datasets by undersampling the over-represented classes to a maximum of 300 samples per class and imposing a hard lower threshold on under-represented families, considering only those categories represented by at least 80 samples. The balanced dataset consists of 2,083 malware samples belonging to 9 families: Adware, Agent, Backdoor, Downloader, Ransomware, Riskware, Trojan, Virus, and Worms.

Metric For Balanced Version of VirusShare Dataset  | HGB | RF | SVM | XGB
-------------     | ------------- | ------------- | ------------- | -------------
Accuracy          | 0.78  	  |0.73		  |0.79		  |0.80
Macro avg. F1       | 0.73	  |0.68		  |0.74		  |0.75
Weighted avg. F1     | 0.78	  |0.72	  	  |0.79		  |0.79



Metric For Imbalanced Version of VirusShare Dataset  | HGB | RF | SVM | XGB
-------------     | ------------- | ------------- | ------------- | -------------
Accuracy          | 0.88  	  |0.77		  |0.89	  	  |0.90
Macro avg. F1       |0.65	  |0.58		  |0.70		  |0.72
Weighted avg. F1     | 0.87	  |0.76		  |0.88		  |0.89		
				
				
XGBoost classifier achieves 80% accuracy for the balanced VirusShare and 90% accuracy for the imbalanced version of the same dataset. On the other hand, the Support Vector Machine classifier achieves 91% and 94% accuracy for the imbalanced and balanced version of the VirusSample dataset.

