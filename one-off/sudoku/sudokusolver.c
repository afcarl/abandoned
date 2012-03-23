#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PUZZLE_ROWS 9
#define PUZZLE_COLS 9
#define POSSIBLE	9
#define BOX_ROWS	3
#define BOX_COLS	3

void print_puzzle();
void print_sudoku_puzzle(int puzzle[PUZZLE_ROWS][PUZZLE_COLS]);
int solve(int puzzle[9][9]);
int solve_completed();
int solve_elimination();
int solve_guess();
int solve_undo();

struct puzzle_state {
	int puzzle[PUZZLE_ROWS][PUZZLE_COLS];
	int possible[PUZZLE_ROWS][PUZZLE_COLS][POSSIBLE];
};

struct puzzle_guess {
	struct puzzle_state *state;
	struct puzzle_guess *prev_guess;
	int row, col, guess;
};

struct puzzle_guess *last_guess;
struct puzzle_state *current_state;

void print_puzzle() {
	print_sudoku_puzzle(current_state->puzzle);
}

void print_sudoku_puzzle(int puzzle[PUZZLE_ROWS][PUZZLE_COLS]) {
	int i, j;
	for (i = 0; i < PUZZLE_ROWS; i++) {
		for (j = 0; j < PUZZLE_COLS; j++) {
			int num = puzzle[i][j];
			if (num > 0) printf("%d|", num);
			else printf(" |");
		}
		printf("\n");
	}
}

int solve(int puzzle[9][9]) {
	int i, j, k;
	
	last_guess = NULL;
	current_state = 
			(struct puzzle_state *) malloc(sizeof(struct puzzle_state));
	memcpy(current_state->puzzle, puzzle, 
			PUZZLE_ROWS*PUZZLE_COLS*sizeof(int));
	
	for (i = 0; i < PUZZLE_ROWS; i++) {
		for (j = 0; j < PUZZLE_COLS; j++) {
			for (k = 0; k < POSSIBLE; k++) {
				current_state->possible[i][j][k] = 1;
			}
		}
	}
	
	/* printf("Received puzzle:\n"); */
	/* print_puzzle(); */

	while (!solve_completed()) {
		if (solve_elimination() != 0) {
			/* printf("LOG: elimination failed\n"); */
			if (solve_undo() != 0) {
				/* printf("LOG: restore not possible!"); */
				return -1;
			} else {
				/* printf("LOG: restored to last state\n"); */
				/* print_puzzle(); */
			}
		} else {
			/* printf("LOG: elimination successful\n"); */
			/* print_puzzle(); */
		}
		
		if (solve_completed()) break;
		else {
			if (solve_guess() != 0) {
				/* printf("LOG: guess not possible!\n"); */
				if (solve_undo() != 0) {
					/* printf("LOG: restore not possible!\n"); */
					return -1;
				} else {
					/* printf("LOG: restored to last state\n"); */
					/* print_puzzle(); */
				}
			} else {
				/* printf("LOG: guess successful\n"); */
				/* print_puzzle(); */
			}
		}
	}

	memcpy(puzzle, current_state->puzzle, 
			PUZZLE_ROWS*PUZZLE_COLS*sizeof(int));
	free(current_state);
	
	while (last_guess != NULL) {
		struct puzzle_guess *temp = last_guess;
		free(last_guess->state);
		last_guess = last_guess->prev_guess;
		free(temp);
	}
	
	return 0;	
}

int solve_completed() {
	int i, j;
	for (i = 0; i < PUZZLE_ROWS; i++)
		for (j = 0; j < PUZZLE_COLS; j++)
			if (current_state->puzzle[i][j] == 0) return 0;
	return 1;
}

int solve_elimination() {
	int i, j, k, m, num;
	int eliminations;
	
	do {
		eliminations = 0;
		for (i = 0; i < PUZZLE_ROWS; i++) {
			for (j = 0; j < PUZZLE_COLS; j++) {
				int left, right, top, bottom;
				int count, num;
				
				if (current_state->puzzle[i][j] > 0) continue;
				
				/* search row */
				for (k = 0; k < PUZZLE_COLS; k++) {
					if (k == j || current_state->puzzle[i][k] == 0) continue;
					
					num = current_state->puzzle[i][k];
					if (current_state->possible[i][j][num-1]) {
						current_state->possible[i][j][num-1] = 0;
						eliminations++;
						/* printf("LOG: (row) eliminating %d from %d,%d\n", 
								num, i, j); */
					}
				}
				
				/* search column */
				for (k = 0; k < PUZZLE_ROWS; k++) {
					if (k == i || current_state->puzzle[k][j] == 0) continue;
					
					num = current_state->puzzle[k][j];
					if (current_state->possible[i][j][num-1]) {
						current_state->possible[i][j][num-1] = 0;
						eliminations++;
						/* printf("LOG: (col) eliminating %d from %d,%d\n", 
								num, i, j); */
					}
				}
				
				/* search box */
				left = (j / BOX_COLS) * BOX_COLS;
				right = left + 3;
				top = (i / BOX_ROWS) * BOX_ROWS;
				bottom = top + 3;
				
				for (k = top; k < bottom; k++) {
					for (m = left; m < right; m++) {
						if (i == k && j == m || 
								current_state->puzzle[k][m] == 0) continue;
						
						num = current_state->puzzle[k][m];
						if (current_state->possible[i][j][num-1]) {
							current_state->possible[i][j][num-1] = 0;
							eliminations++;
							/* printf("LOG: (box) eliminating %d from %d,%d\n", 
									num, i, j); */
						}
					}
				}
				
				/* check for completion */
				count = 0;
				for (k = 0; k < POSSIBLE; k++) {
					if (current_state->possible[i][j][k]) {
						count++;
						num = k+1;
					}
				}
				
				if (count == 1) {
					current_state->puzzle[i][j] = num;
					/* printf("LOG: %d,%d is now %d\n", i, j, num); */
				} else if (count == 0) {
					/* printf("LOG: no availabilities on %d,%d!\n", i, j); */
					return -1;
				}
			}
		}
	} while (eliminations > 0);

	return 0;
}

int solve_guess() {
	int row, col, guess, k, done;
	
	done = 0;
	guess = 0;
	for (row = 0; row < PUZZLE_ROWS && !done; row++) {
		for (col = 0; col < PUZZLE_COLS && !done; col++) {
			if (current_state->puzzle[row][col] == 0) {
				for (k = 0; k < POSSIBLE && !done; k++) {
					if (current_state->possible[row][col][k] == 1) {
						guess = k+1;
						/*
				printf("LOG: guessing %d on %d,%d\n", guess, row, col);
				        */
						done = 1;
					}
				}
				
				/* no more possibilities! */
				if (guess == 0) {
					/*
			    printf("LOG: no more possibilities on %d,%d!\n", row, col);
			        */
					return -1;
				}
			}
		}
	}
	
	if (guess == 0) {
		/* printf("LOG: no possibilities for guessing!\n"); */
		return -1;
	}

	row--, col--;
	struct puzzle_state *new_state = 
			(struct puzzle_state *) malloc(sizeof(struct puzzle_state));
	memcpy(new_state, current_state, sizeof(struct puzzle_state));
	new_state->puzzle[row][col] = guess;
	
	struct puzzle_guess *new_guess =
			(struct puzzle_guess *) malloc(sizeof(struct puzzle_guess));
	new_guess->state = current_state;
	new_guess->prev_guess = last_guess;
	new_guess->guess = guess;
	new_guess->row = row;
	new_guess->col = col;
	last_guess = new_guess;
	
	current_state = new_state;
	return 0;
}

int solve_undo() {
	int row, col, guess;
	if (last_guess == NULL) return -1;
	
	free(current_state);
	current_state = last_guess->state;
	row = last_guess->row;
	col = last_guess->col;
	guess = last_guess->guess;
	current_state->possible[row][col][guess-1] = 0;
	free(last_guess);
	last_guess = last_guess->prev_guess;	
	
	return 0;
}

int main(int argc, char **argv) {
    int puzzle[9][9];
    FILE *in_file;
    char line[80];
    int i, j;
              
    printf("Sudoku Solver\n");
    printf("Using input file: %s\n", argv[1]);
    
    in_file = fopen(argv[1], "r");
    for (i = 0; i < 9; i++) {
        fgets(line, 80, in_file);
                
        for (j = 0; j < 9; j++) {
            puzzle[i][j] = line[j] - '0';
            if (puzzle[i][j] > 9)
                puzzle[i][j] = 0;
        }
    }
    
    printf("Puzzle:\n");
	print_sudoku_puzzle(puzzle);

    solve(puzzle);
	
	printf("Solved:\n");
	print_sudoku_puzzle(puzzle);
}
