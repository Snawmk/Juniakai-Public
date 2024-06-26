<img src="https://github.com/Snawmk/Juniakai/blob/main/juniakai.png?raw=true" alt="Juniakai Group">

Juniakai is the youth group of the Youth Department at the Japan-Brazil Institute of Campinas.

To assist in the management activities of the Juniakai youth group, we use a Google spreadsheet to track important information such as the **attendance** of the youth at meetings, payment of **membership fees**, and **registration** of their personal data. Additionally, other important information is stored there, such as financial control, cash inflows and outflows, and a record of how much the group owes to Nipo monthly.

To manage this information, we use Google Sheets to facilitate collaboration among the people involved, as its use is similar to the well-known Microsoft Excel and it can be easily shared for simultaneous integration and collaboration, requiring only a GMAIL account.

Weekly, we need to manually update the spreadsheet with some information, such as new youth registrations and tracking the attendees of the day. This project aims to ease the administrator's workload by automating some tasks and ensuring that the control is consistent automatically.

For this, some needs were outlined:

- Verify if all youth marked as ACTIVE in the spreadsheet are attending Juniakai meetings on Sundays and identify who is not complying with this rule.
- Identify upcoming birthdays.
- Automatically mark as “debt” those who have not paid the previous month's membership fee.
- Automatically fill in the total amount due each month to be paid to Nipo regarding the membership fees.
- Check if the Juniakai group includes all who should be members.

To meet these specific needs, we developed some Python scripts to automate these processes, and some outputs from these scripts are written directly into the Juniakai spreadsheet and send informational messages on DISCORD or Whatsapp using third-party APIs. These codes are stored in a version control repository on Github. Additionally, to effectively run the Python codes firstly we created a free tier virtual machine with one year of validity on Amazon AWS. Now, the codes are running in Amazon Lambda.

