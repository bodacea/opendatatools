### Page1 information objects

* Dropbox.
* Desktop. An executable script (e.g. RSSXML.py) is executed in the appropriate Dropbox desktop folder creating the necessary XML file [including folders, sub-folders and files].
* Web server. Content could be viewed via a webpage directly from the web server.
* Mobile phone. iPhone/iPad on IOS; Android,Blackberry, Nokia on Java, MS Mobile on Windows7. Note: Folders should appear as folder-like icons within the application so user know to touch/select to open for more content. Two views: 1) swipe through all documents, 2) all folders/docs are represented by larger icons and user selects to view
* Laptop. 
* Websites. 
* Flow from Dropbox to desktop: Two way document flow between desktop client and Dropbox server. Content held in a private folder but exposed with ‘shareable’ link. [Example link](http://db.tt/oWCAod0O) [files not representative]
* Flow from Dropbox to web server: Custom desktop/server app downloads content into a user specified directory [which could represent a folder on a web server]
* Flow from Dropbox to mobiles, laptops, websites: One way. Clients read specific RSS.XML and download relevant documents
* Flow from Dropbox to mobiles: Mobile phones download content [user specifies if automatic update or only manual]
* Flow from Dropbox to Laptop. Custom desktop app download and displays content
* Flow from Dropbox to websites: Websites use an RSS read to display content.
* Example content on mobile, laptop, websites, web server is: maps, appeals, situation report, emergency numbers. Example content on desktop is maps, appeals, situation report, emergency numbers, RSS.xml, RSSXML.py. 

### Explanations and Priorities of items on first page

The PowerPoint diagram in the project description contains the following footnotes: 

1 An executable script accepts a URL input [provided by the user on first execution – which comes from a shareable link in a private dropbox folder] and generates an XML file. The XML file mirrors the directory of the folder in which it is executed [including document and sub-folders]. The resulting XML must be readable by RSS readers

2 Other than those given access through dropbox [and can use the dropbox client] all files will only be downloaded to their machine/phone/tablet using the Dropbox API to fetch the files/folders specified in the XML file.

3 Mobile phones download and display the folders and documents.

1. Add Kiosk: From the home screen of HK2, the user choose to ‘Add Kiosk’ and are prompted with a list of available kiosk. The available kiosks are fed from an [RSS
feed](https://spreadsheets.google.com/feeds/list/0At0Y9gPUymOmdHRkeEN5N1JHdEFEWXdfeFdlUEZUMHc/od6/public/basic?hl=en_US&alt=rss)
2. Sync: by default, every Kiosk added to the application is ‘manual’ sync. User should be able to specify automatic sync and choose Wi-Fi only or Mobile & Wi-Fi. These settings need to be specified by kiosk [versus overall] as users might want to sync one at all times and others on Wi-Fi only.

4 Applications should be built for both iPhone and iPad. However, it would be best to initially develop for a base iOS and then only customize if necessary

5 Develop one mobile client in a Java base so that it can be purposed across many different devices. Android is priority 1, BB is priority 2, and others are priority 3

6 Develop a mobile client for Windows 7 Mobile

7 A one-way syncing tool for desktop computer user would ensure that users can have their files even when not using one of their portable devises. As well, they may want to sync more kiosks on their desktop than on their mobile device(s). Users can specify where the files are synced to on their machine.

8 If developed correctly, the XML file could be consumed by any website that can display an RSS feed. In this case, the content of the HK2 would be displayed on the Humanitarian Response website.

9 By leveraging #7 on a web server, the contents of the HK2 could be downloaded into a specific directory which is displayed on a website. This setup would also give interesting possibilities for distributed management of contents of a website [especially for those in the emergency area --- simply adding a file to dropbox and the website gets updates on the next sync. Note: there would have to be regular sync of the files onto the server.

Items 1,2,3,4,5,8 are priority 1 for development. 7 is priority 2, 6 and 9 are priority 3.
