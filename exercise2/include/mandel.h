#ifndef MANDELBROT_H__
#define MANDELBROT_H__

// ------------------------------- INCLUDES ------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <time.h>
#include <complex.h>

#if defined(_OPENMP)
	#include <omp.h>
#endif

// -------------------------------- MACROS -------------------------------------

#if defined(_OPENMP)
	// Measure the wall-clock time
	#define CPU_TIME (clock_gettime(CLOCK_REALTIME, &ts), \
					(double)ts.tv_sec + (double)ts.tv_nsec * 1e-9)

	// Measure the cpu thread time
	#define CPU_TIME_th (clock_gettime(CLOCK_THREAD_CPUTIME_ID, &myts), \
						(double)myts.tv_sec + (double)myts.tv_nsec * 1e-9)
#else
	// Measure the cpu process time
	#define CPU_TIME (clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts), \
					(double)ts.tv_sec + (double)ts.tv_nsec * 1e-9)
#endif

// Default values
#define W_dflt 1000
#define H_dflt 1000
#define Xmin_dflt -2.0
#define Xmax_dflt 2.0
#define Ymin_dflt -2.0
#define Ymax_dflt 2.0
#define Imax_dflt 1000

// ------------------------------- FUNCTIONS -----------------------------------

// Function to calculate the number of iterations for a given pixel
static inline unsigned short int mandelbrot(const complex double c, 
                                            const int I_max) {
    complex double z = 0.0;
    unsigned short int i = 0;
    while (cabs(z) < 2.0 && i < I_max) {
        //TODO: remove. z = f_c(z, c);)
        z = z * z + c;
        i++;
    }
    return i;
}

// Function to write the image to a pgm file
void write_pgm_image(unsigned short int **image, int maxval, 
                     int xsize, int ysize, const char *image_name) {

    FILE* image_file; 
    image_file = fopen(image_name, "w"); 

    int color_depth = 1 + ( maxval > 255 );

    fprintf(image_file, "P5\n# generated by\n# put here your name\n%d %d\n%d\n", 
            xsize, ysize, maxval);
  
    // Write each row to the file
    for (int i = 0; i < ysize; i++) {
        fwrite(image[i], 1, xsize * color_depth, image_file);
    }

    fclose(image_file); 
}

double mean(double *data, int size) {

	double sum = 0;
	for (int i = 0; i < size; i++)
		sum += data[i];
	return sum / size;
}

double min(double *data, int size) {
	double min = data[0];
	for (int i = 1; i < size; i++)
		if (data[i] < min)
			min = data[i];
	return min;
}

double max(double *data, int size) {
	double max = data[0];
	for (int i = 1; i < size; i++)
		if (data[i] > max)
			max = data[i];
	return max;
}

double stdev(double *data, int size) {
	double avg = mean(data, size);
	double sum = 0;
	for (int i = 0; i < size; i++)
		sum += (data[i] - avg) * (data[i] - avg);
	return sqrt(sum / size);
}

#endif // MANDELBROT_H__
