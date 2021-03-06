#define LIMIT 1000 

#define LUCKY_NUM 9

#define enemysRollsNum(die, level) rand()     // PLACEHOLDER! Redefined in game.c 

int fd ;

uint8_t rand_vals[LIMIT] ;

void init(){
	srand(time(0)) ;
	fd = open("/dev/urandom", O_RDONLY) ;
}

uint32_t a_very_random_number(){			// Fair and unpredictable!
	float sum = 0 ;
       	if (read(fd, rand_vals, sizeof(uint8_t) * LIMIT) & 0x80000000)
		return 0 ;
	for (uint32_t i = 0 ; i < LIMIT ; i++, sum += (float)rand_vals[i] / (uint8_t)(~0)) ;
	return (uint32_t)sum ;  
}

uint32_t diceRollsSum(uint8_t sides, uint32_t times){	
	read(fd, rand_vals, sizeof(uint8_t)) ;
	srand(rand_vals[0]) ; 
	uint32_t sum = 0 ;
	for (uint32_t i = 0 ; i < times ; i++, sum += (1 + rand() % sides)) ;   // Works just like a real die!
	return sum ;
}

// TO DO: move this to game.c

int8_t resultsCompare(	uint8_t yourDie,	// A die chosen by player 
			uint8_t enemysDie, 	// A die chosen by enemy 
			uint8_t rollsNum,	// How many times player rolls it  
		       	uint8_t enemysLevel){
	uint8_t yourSum, enemysSum ;	
	uint32_t randomNum = a_very_random_number() ; // A number generated by a computer 
	for (uint32_t i = 0 ; i < enemysLevel - 1 ; i++, randomNum += a_very_random_number()) ; // A bit of complexity for high-leveled enemies
	yourSum = diceRollsSum(yourDie, rollsNum) ; 
	enemysSum = diceRollsSum(enemysDie, enemysRollsNum(enemysDie, enemysLevel)) ;
	return abs((int)(yourSum - randomNum)) <= abs((int)(enemysSum - randomNum)) ;
}
