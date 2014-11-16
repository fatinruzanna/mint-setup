Setup Oracle JDK6
==================

Installing Oracle JDK6
----------------------

1. Add webupd8team apt repository for Oracle Java

		(sudo) add-apt-repository ppa:webupd8team/java
		(sudo) apt-get update
		(sudo) apt-get install oracle-java6-installer


2. Follow instructions to install. Once installed, you may check the version with:

		java -version


	You should see the following in your terminal:

		java version "1.6.0_45"
		Java(TM) SE Runtime Environment (build 1.6.0_45-b06)
		Java HotSpot(TM) 64-Bit Server VM (build 20.45-b01, mixed mode)


3. If you're not using version 1.6.0.x by Oracle (e.g. OpenJDK's version), run the following command to update the Java version to use:

		(sudo) update-java-alternatives -s java-6-oracle


	Ignore any warnings that pop-up. You may run the command in the previous step to check the version again. Available versions can be checked at /usr/lib/jvm.


4. To set Oracle JDK6 environment variables correctly, run the following command:

		(sudo) apt-get install oracle-java6-set-default



**References:**
* http://www.webupd8.org/2012/01/install-oracle-java-jdk-7-in-ubuntu-via.html
