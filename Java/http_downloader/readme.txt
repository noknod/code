�������:
���������� ������� ��� ���������� ������ �� HTTP ���������.

- - -

������������ ������� ���������� � ������������
Windows XP SP 2

������ Java
java version "1.6.0_21"
Java(TM) SE Runtime Environment (build 1.6.0_21-b07)
Java HotSpot(TM) Client VM (build 17.0-b17, mixed mode, sharing)

- - -

��������� ������ � ����� � �������

http_downloader
	|
	-	out		����� ��� �������� �������� ������
		|
		-	(out.txt)		�� ����� ������ ������� ��� ������������ � ���� ����
		-	(err.txt)		�� ����� ������ ������� ������� ������ ������������ ����
		-	(*.bmp/jpg)		��������� ����� �� ����� ������ �������

	-	prog		����� � ��������� ������ � ������ ��� �������� ������������ ������
		|
		-	src			����� � ��������� ������
		-	build.xml		���� ��� �������� ������������ ������ ����������� ant
		-	(build\classes)	����� ���������� ant ������� ��� ����� � ����-������ �������
		-	(dist\lib)		��������� ant`�� ���������� ����� �������� � ��� �����
		-	(dist\kyatest.jar)	�������� ����������� �����-�������

	-	make.bat	make-����, ������������ ant ��� ������

	-	run.bat	bat-���� � �������� ������, ���������� test.txt ��� �������� ������

	-	test.txt	���� � ��������� ������ ��� ����������

	-	readme.txt	�������������� ������ ���� �� ��������

- - -

�������� ����������� �����, �������� ������, ����� ������ ant`�� � ����� prog\dist\ ��� ������ download.jar.

�� ���� ����������� ���������

	-n  ���������� ������������ �������� ������� (1,2,3,4....)
	-l   ����� ����������� �� �������� ����������, ��� ���� �������, ����������� - ����/�������, 
		����� ������������ �������� k,m (k=1024, m=1024*1024)
	-f   ���� � ����� �� ������� ������
	-o  ��� �����, ���� ���������� ��������� �����
	-ml ���� ��� ������ ���� �� ����� ������, ���� ����� sys, �� ��� ����� ������������ � ����������� ����� 
 		������ ���������, ��� ���������� ��������� ����������� ������� �� �����
	-me ���� ��� ������ ������� ������ �� ����� ������, ���� ����� sys, �� ��� ����� ������������ � ����������� 
		����� ������ ������, ���������� ��������� ���������� ������� ��� ��������� sys

������ ����� �� ��������:

	<HTTP ������><������><��� �����, ��� ������� ��� ���� ���������>

�� �������, � HTTP ������ ��� ��������, ��� encoded �������� - ��� ������ ������� ������ � ����������� ��������� ��� ����������� ��������.
������ ��������� ��� ������������ �����������. ����� �������������� ������ HTTP-��������.

�� �������, ������ ����� ����������� � �����, �� � ������� ������� ��� ����������. � ���� ������ ��������� �������� ��� ��������� ���� � 
������ ������. ���������, ��� ����� ������ ���������.
���� ������� ������� ���������� �� ����������� �����, ����� ���� (���������) ������� ��������� �������, � ��������� ������ �������.
�� ���� ������ ���������� ������ ���� map-reduce ��� ������, � ����� ���������� �� ������ ������� ���� ���������� �, ��������, ���������
�����������.

� ����� ������ ��������� ������� ���������� - ����� ������, ���������� ��������� ����, ����� ������������� ������ � ���������� ������ 
��� ���������� � �����������.