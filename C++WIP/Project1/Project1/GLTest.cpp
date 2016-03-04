#include <GL/freeglut.h>
#include<vector>
#include <string>
#include <fstream>
#include <sstream>

using namespace std;

int init_width = 1200, init_height = 800; //Initial window resolution variables
int winPosX = 0, winPosY = 0; //Initial window position variables
char winTitle[] = "Project 2 ALL"; //Window caption
float angle = 0.0f; //Debug variable for spinning models
float fov = 45.0f; //Camera's Field Of View in degrees


vector<vector<float>> objLoad(string path) { //Our OBJ 3D model loading function 


	vector<vector<float>> vertices, UV, normals; //Store XYZ vertex co-ordinates using a vector in a vector
	unsigned i = 0;
	vector<vector<int>> vertexFace;

	vertices.push_back(vector<float>());

	string line;

	ifstream objFile(path); //Open the file path given to the function


	while (getline(objFile, line)) {

		string h = line.substr(0, 2); //Line header, tells us what the line is defining

		if (h == "v ") { //If line contains vertex definition

			vector<string> temp_vector; //Vector to hold strings for this method
			vector<float> temp_vector2; //Vector to hold floats for this method
			string temp_line = line.substr(2), temp_str; //Remove line header
			int temp_int; //Temporary variable for int/string conversion

			stringstream ss(temp_line); //Make the current line act as an input stream

			while (ss.good()) //Method to separate the string by spaces, while loop terminates at end of string
			{
				getline(ss, temp_str, ' ');
				if (temp_str.size() != 0) { temp_vector2.push_back(stof(temp_str)); } //Do not allow adding empty values to vector
			}

			vertices.push_back(temp_vector2);

		}
		else if (h == "vt") { //If line contains UV definition


		}
		else if (h == "vn") { //If line contains vertex normal definition

		}
		else if (h == "f ") { //If line contains face definition


			vector<string> temp_vector; //Vector to hold strings for this method
			vector<int> temp_vector2, temp_vector3; //Vector to hold ints for this method
			string temp_line = line.substr(2), temp_str; //Remove line header

			stringstream ss(temp_line); //Make the current line act as an input stream

			while (ss.good()) //Method to separate the string by spaces, while loop terminates at end of string
			{
				getline(ss, temp_str, ' ');
				if (temp_str.size() != 0) { temp_vector.push_back(temp_str); } //Do not allow adding empty values to vector
			}

			for each(string k in temp_vector) { //For each vector, separate each string by forward slashes

				stringstream ss(k);

				while (ss.good())
				{
					getline(ss, temp_str, '/');

					string temp_str2 = temp_str;

					if (temp_str.size() != 0) { temp_vector2.push_back(stoi(temp_str2)); }

				}

			}

			if (temp_vector2.size() != 0) {

				temp_vector3.push_back(temp_vector2[0]);
				temp_vector3.push_back(temp_vector2[2]);
				temp_vector3.push_back(temp_vector2[4]);
				vertexFace.push_back(temp_vector3);

			}

		}
		i++;
	}

	vector<vector<float>> finalVec;
	for each(vector<int> vecI in vertexFace) {
		for each(int id in vecI) {
			finalVec.push_back(vertices[id]);
		}
	}

	return finalVec;

}





void changeSize(int w, int h) {

	float aspect = float(w) / float(h); //Get aspect ratio from window resolution

										// PROJECTION allows us to transform the camera projection, i.e. edit FOV, aspect ratio, clipping
	glMatrixMode(GL_PROJECTION);

	//Load identity matrix to reset projection matrix
	glLoadIdentity();

	// Resize display size to window size
	glViewport(0, 0, w, h);

	// Camera properties reset
	gluPerspective(fov, aspect, 0.1f, 100.0f);

	// MODELVIEW allows us to transform objects in the world
	glMatrixMode(GL_MODELVIEW);

}

void renderScene(void) {
	//Function to render all objects in the current scene

	// Clear Color and Depth Buffers
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	// Reset transformations
	glLoadIdentity();
	// Set the camera
	gluLookAt(0.0f, 0.0f, 10.0f,
		0.0f, 0.0f, 0.0f,
		0.0f, 1.0f, 0.0f);

	glRotatef(angle, 0.0f, 1.0f, 0.0f);

	glRotatef(90.0f, 1.0f, 0.0f, 0.0f);

	//glTranslatef(0, 0, 0);

	//glColor3f(1.0f, 0.0f, 0.0f);

	vector<vector<float>> arrayBuffer = objLoad("test.obj");


	glBegin(GL_TRIANGLES);
	for each(vector<float> vertex in arrayBuffer) {
	glVertex3f(vertex[0], vertex[1], vertex[2]);
	}
	glEnd();

	angle += 0.1f;

	glutSwapBuffers();

}

int main(int argc, char** argv) //Main function, parameters are used for initialising GLUT
{
	glutInit(&argc, argv); //Initialises GLUT, parameters necessary for initiliasation
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE| GLUT_RGBA);  //DEPTH: Enables 3D, DOUBLE: Enables double buffering, RGBA: Colour with alpha
	glutInitWindowSize(init_width, init_height);
	glutInitWindowPosition(winPosX, winPosY);
	glutCreateWindow(winTitle);

	//glEnable(GL_DEPTH_TEST);

	glutDisplayFunc(renderScene);
	glutReshapeFunc(changeSize);
	glutIdleFunc(renderScene);

	glutMainLoop();
	return 1;
}