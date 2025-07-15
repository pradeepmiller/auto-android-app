# auto-android-app

# This is sample Android app project which has the below:
#   - 1) A Locator IDs for automation available in the 'AutomationIds.kt' file.
#   - 2) A Python script - 'kt_to_java_converter.py', which reads the above mentioned kt file and convert it into a java format.
#   - 3) A yaml / yml file - 'convert_automationids_kt_to_java.yml', which auto triggers the workflow whenever there is a change in the kt file mentioned in the point-1 above and generate a java file - 'AutomationIdLocatorsAndroid.java' in the utils directory (the same path where the 'AutomationIds.kt' file resides).
