#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <math.h>
#include <time.h>
#include "rand.h"
#include "figures.h"

#define LUCKY_NUM 9

#define BUF_SIZE 256

#define INDENT_COUNT "49"

#define TEXT_BLOCK_SIZE 70

#define STANDART_SLEEP_TIME 1

#define TEXTLINE_SPEED 20000

#define IMAGE_SPEED 40000

#define enemyRollsNum(lev, die) (uint32_t)(LIMIT / 2 * lev + ((int32_t)(2*rand() % 2 - 1) * rand() % (LUCKY_NUM*9))) * 2 / die

#define BATTLE_SLEEP 1500000

uint8_t* snowman_lines[3] =
	{
		"The snowman is ready to use its carrot! The nose one!",
		"You wonder if this classifies as beating up local fauna.",
		"The snowman's arm branches are surprisingly effective at holding      several dice at a time!"
	} ;

uint8_t* accountant_lines[3] =
	{
	 	"Did he just say, \"Come with me if you want to live\"? Must be a        Terminator fan!",
		"Did he just say, \"Live for nothing or die for something\"? Must        be a Rambo fan!",
		"Did he just say, \"I should've broke your thumb\"? Must be a Rocky fan!"
	} ;

uint8_t* reindeer_lines[3] =
	{
	"The reindeer's legs are really good at rolling dice, he sure isn't    using those for kickin'!", 
	"You hypothesize that the planned attack on you is him finally feeling fed up with overworking in the service industry.",
	"You're trying to remember all Santa's reindeers' names. This one sure looks like Rudolph."
	} ;

uint8_t* train_lines[3] = 
	{
	"You reminisce of a childhood trauma, getting run over buy a toy train like this after exiting a cafe shop.",
	"Would your stepping off the tracks classify as skipping a turn?",
	"In the best traditions of a gundam anime, the train's frontal plate   resembles a growly face obsessed with vengeance."
	} ;

uint8_t* conductor_lines[3] =
	{
	"The conductor must've been sleeping during his shift, making him even angrier as a result. That thing's on autopilot, anyway!",
	"The conductor looks helpless for a second, thinking about other real  conductors making fun of him.",
	"You wonder what the max passenger count this guy has ever seen on his train is."
	} ;

uint8_t* elf_lines[3] =
	{
	"You judge the elf's sense of style, the gaudy red and green together especially.",
	"His height being all midget-like, you honestly feel like you're attacking a child.",
	"You let out a sign, thinking how those presents from the bag may have been yours if not for your brutal honesty."
	} ;

uint8_t* giftbox_lines[3] = 
	{
	"The gift box shuffles making strange noises, but it's all Greek to      you.",
	"With wrapper paper now torn to pieces and mostly gone, this might as well not be a Christmas gift anymore.",  
	"A fighting gift box is kind of unimaginitive, unless you think of everything that can possibly be inside it."
	} ;

uint8_t* mimic_lines[3] = 
 	{
	"THIS. IS. ALL. YOUR. FAULT.",
	"It really is a jack-in-a-box, but a seriously bone-chillingly creepy one!",
	"The constant springing noise will most definitely start grating on your ears soon."
	} ;

uint8_t* tree_lines[3] = 
	{
	"The tree is sparkling and shining terrifically.",
	"On closer look, you realize the \"MERRY CHRISTMAS\" letters are paper cut-outs, not a garland. What a cheap solution!",
	"You are praying that a giant tree is not the game's actual final boss."
	} ;

uint8_t* santa_lines[3] =
	{
	"Santa's got a katana on his back, but isn't using it. Maybe it's just for show. Or maybe he's secretly a weeb?",
	"Santa coughs uncontrollably. You wonder what kind of genius decides to carry out a world domination plan in his eighties.",
	"Santa's not ready to lose in a dice battle, but it's logical to assume he doesn't have time to play board games anyways."
	} ;

uint8_t buffer[BUF_SIZE] ;

int32_t hp = 100 ;

uint8_t level = 1 ;

uint8_t diceTypes[11] = {4, 6, 8, 10, 12, 14, 16, 20, 24, 26, 30} ;

uint8_t candies = 2 ;

uint8_t readChar(){
	uint8_t input ; 
	input = getc(stdin) ;
	while (input == '\n')
		input = getc(stdin) ;
	while(getc(stdin) != '\n') ;
	return input ;
}

int8_t fight(const uint8_t* enemyName, uint8_t enemyLevel, int32_t enemyInitialHP, uint32_t baseDamage, const uint8_t** lines){
	uint8_t dice[4] = {diceTypes[rand() % 11], diceTypes[rand() % 11], diceTypes[rand() % 11], diceTypes[rand() % 11]} ;
	uint8_t input, enemyDie, lineNum ;	
	int32_t yourHp = hp, enemyHp = enemyInitialHP ; 
	uint32_t round = 1, rollsNum, randomNum, yourSum, enemySum ;
	while (1){
		printf("\n%"INDENT_COUNT"s", "") ;
		printf("                               Round %d:\n", round++) ; 
		usleep(BATTLE_SLEEP) ;
		printf("\n%"INDENT_COUNT"s", "") ;
		printf("Your HP is %d", yourHp) ; 					
		printf("\n%"INDENT_COUNT"s", "") ;
		printf("%s's HP is %d\n", enemyName, enemyHp) ;
		usleep(BATTLE_SLEEP) ;
		if (rand() % 3){
			printf("\n%"INDENT_COUNT"s", "") ;
			lineNum = rand() % 3 ;
			printCenteredString(lines[lineNum], strlen(lines[lineNum])) ;
			puts("") ;
		}
		printCenteredString("The dice available:\n", 20) ; 
		for (int i = 0 ; i < 4 ; i++){
			usleep(150000) ;
			printf("\n%"INDENT_COUNT"s", "") ;
			printf("%c.   %d-sided\n", 'a' + i, dice[i]) ;
		}
		printCenteredString("Which die do you want to pick? ", 31) ;
		input = readChar() ;
		if (input < 'a' || input > 'd'){
			printCenteredString("Oh no! You hesitated too much and have skipped a precious turn.\n", 64) ;	
			usleep(BATTLE_SLEEP) ;
			goto ENEMY_STRIKES ;
		}	
		else{
			printf("\n%"INDENT_COUNT"s", "") ;
			printf("How many times do you want to roll the die? ") ;
			scanf("%d", &rollsNum) ;
			if (rollsNum > 5000){
				printCenteredString("The dice managed to disintegrate one by one from the crazy amount of  hitting the floor. Maybe not throwing so much next time?\n", 127) ;	
				usleep(BATTLE_SLEEP) ;
				goto ENEMY_STRIKES ;

			}
		}
		randomNum = 0 ; 
		for (uint32_t i = 0 ; i < enemyLevel ; i++, randomNum += a_very_random_number()) ;
		yourSum = diceRollsSum(dice[input - 'a'], rollsNum) ; 
		enemyDie = dice[rand() % 4] ;
		enemySum = diceRollsSum(enemyDie, enemyRollsNum(enemyLevel, enemyDie)) ;
		printf("\n%"INDENT_COUNT"s", "") ;
		printf("You roll %d-sided die %d times, resulting %d\n", dice[input - 'a'], rollsNum, yourSum) ;
		usleep(BATTLE_SLEEP) ;
		printf("\n%"INDENT_COUNT"s", "") ;
		printf("%s rolls %d-sided die, resulting %d\n", enemyName, enemyDie, enemySum) ;
		usleep(BATTLE_SLEEP) ;
		if (abs(((int32_t)yourSum - randomNum)) <= abs(((int32_t)enemySum - randomNum))){
			printf("\n%"INDENT_COUNT"s", "") ;
			printf("You were closer to the random number this time!\n") ;
			usleep(BATTLE_SLEEP) ;
			goto YOU_STRIKES ;
		}
		else{ 
			printf("\n%"INDENT_COUNT"s", "") ;
			printf("%s was closer to the random number this time!\n", enemyName) ;
			usleep(BATTLE_SLEEP) ;
			goto ENEMY_STRIKES ;
		}
ENEMY_STRIKES:
		if (rand() % 16){
			yourHp -= baseDamage ;
			printf("\n%"INDENT_COUNT"s", "") ;
			printf("%s strikes you, making you lose %d HP\n", enemyName, baseDamage) ;
		}
		else{
			yourHp -= baseDamage*2 ;
			printf("\n%"INDENT_COUNT"s", "") ;
			printf("%s critically strikes you, making you lose %d HP\n", enemyName, baseDamage) ;
		}
		goto BATTLE_RESULTS ;
YOU_STRIKES:
		if (rand() % 16){
			enemyHp -= 25*level ;
			printf("\n%"INDENT_COUNT"s", "") ;
			printf("You strike %s, making the enemy lose %d HP\n", enemyName, 25*level) ;
		}
		else{
			enemyHp -= 25*level*2 ;
			printf("\n%"INDENT_COUNT"s", "") ;
			printf("You critically strike %s, making the enemy lose %d HP\n", enemyName, 25*level*2) ;
		}
BATTLE_RESULTS:
		if (yourHp <= 0)
			return 1 ;
		if (enemyHp <= 0)
			return 0 ;
		for (uint8_t i = 0 ; i < 4 ; i++)
			dice[i] = diceTypes[rand() % 11] ;
		if (candies > 0 && yourHp < hp){
			usleep(BATTLE_SLEEP) ;
			printf("\n%"INDENT_COUNT"s", "") ;
			printf("Would you like to use a candy to restore some HP?") ;
			printf("\n%"INDENT_COUNT"s", "") ;
			printf("You have %d candies in your pocket (y/n) ", candies) ;
			input = readChar() ;
			if (input == 'y' || input == 'Y'){
				candies-- ;
				yourHp += 20*level ;
				printf("\n%"INDENT_COUNT"s", "") ;
				printf("You use a candy. %d HP restored\n", 20*level) ;
			}
		}	
		usleep(BATTLE_SLEEP) ;
	}
}

void printLines(FILE* fd){
	uint32_t i ;
	while(1){
		fgets(buffer, BUF_SIZE, fd) ;
		if (buffer[0] == '#'){
			return ;
		}
		printf("%"INDENT_COUNT"s", "") ;
		i = 0 ;
		while (buffer[i] != '\0'){
			fputc(buffer[i++], stdout) ;
			usleep(TEXTLINE_SPEED) ;
		}
	}
}

void skipLines(FILE* fd){
	while(1){
		fgets(buffer, BUF_SIZE, fd) ;
		if (buffer[0] == '#'){
			return ;
		}
	}
}

void printCenteredString(const uint8_t* string, uint32_t size)
{
	uint32_t count = 0, i, len ;
	while (count < size){
		printf("\n%"INDENT_COUNT"s", "") ;
		len =  size - count > TEXT_BLOCK_SIZE ? TEXT_BLOCK_SIZE : size - count ;
		strncpy(buffer, string + count, len) ;
		buffer[len] = '\0' ;
		count += TEXT_BLOCK_SIZE ;
		i = 0 ;
		while (buffer[i] != '\0'){
			fputc(buffer[i++], stdout) ;
			usleep(TEXTLINE_SPEED) ;
		}
	}
}

void levelUp(){
	level++ ;
	printCenteredString("Level up!\n", 10) ;
	hp += 50 * (level - 1) ;
}

void rip(){
	sleep(STANDART_SLEEP_TIME) ;
	printCenteredString("You lose!\n", 10) ;
	printCenteredString("You weren't able to overcome your enemy and are now planning your     escape. The mall mystery's resolution is incomplete as you are forced to flee the battlefield.\n", 165) ;
	printCenteredString("                              GAME OVER\n\n", 41) ;

}

void printImage(const uint8_t* string, uint32_t size, uint32_t lineNum)
{
	uint32_t count = 0, len ;
	while (count < size){
		printf("\n%"INDENT_COUNT"s", "") ;
		len =  size - count > TEXT_BLOCK_SIZE ? TEXT_BLOCK_SIZE : size - count ;
		strncpy(buffer, string + count, len) ;
		buffer[len] = '\0' ;
		count += TEXT_BLOCK_SIZE ;
		printf("%s", buffer) ;
		usleep(IMAGE_SPEED) ;
	}
}
void printTitle(){
	for (uint32_t i = 0 ; i < 9 ; i++){
	       puts(title[i]) ;	
		usleep(100000) ;
	}
	puts("") ;
}

void printMessage(){
	for (uint32_t i = 0 ; i < 39 ; i++)
	       printImage(phone[i], 44, i) ;	
	puts("\n") ;
}

void snowmanApproaches(){
	puts("") ;
	for (uint32_t i = 0 ; i < 18 ; i++){
		printImage(snowman[i], 52, i) ;
	}
	puts("\n") ;
}

void accountantApproaches(){
	puts("") ;
	for (uint32_t i = 0 ; i < 29 ; i++)
		printImage(accountant[i], 36, i) ;
	puts("\n") ;
}

void reindeerApproaches(){
	puts("") ;
	for (uint32_t i = 0 ; i < 27 ; i++)
		printImage(reindeer[i], 67, i) ;
	puts("\n") ;
}

void trainApproaches(){
	puts("") ;
	for (uint32_t i = 0 ; i < 17 ; i++)
		printImage(train[i], 70, i) ;
	puts("\n") ;
}

void conductorApproaches(){
	puts("") ;
	for (uint32_t i = 0 ; i < 16 ; i++)
		printImage(conductor[i], 32, i) ;
	puts("\n") ;
}


void elfApproaches(){
	puts("") ;
	for (uint32_t i = 0 ; i < 27 ; i++)
		printImage(elf[i], 62, i) ;
	puts("\n") ;
}

void giftboxApproaches(){
	puts("") ;
	for (uint32_t i = 0 ; i < 19 ; i++)
		printImage(giftbox[i], 53, i) ;
	puts("\n") ;
}

void mimicApproaches(){
	puts("") ;
	for (uint32_t i = 0 ; i < 26 ; i++)
		printImage(mimic[i], 28, i) ;
	puts("\n") ;
}

void treeApproaches(){
	puts("") ;
	for (uint32_t i = 0 ; i < 47 ; i++)
		printImage(tree[i], 70, i) ;
	puts("\n") ;
}

void santaApproaches(){
	puts("") ;
	for (uint32_t i = 0 ; i < 31 ; i++)
		printImage(santa[i], 48, i) ;
	puts("\n") ;
}

int8_t firstScene(FILE* fd){
	uint8_t choice ;
	printf("\033[H\033[J") ;
	printTitle() ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
ENTRANCE_CHOICE:
	printCenteredString("Your choice (y/n): ", 19) ;
	choice = readChar() ;
	if (choice == 'n' || choice == 'N'){
        	printLines(fd) ;
		puts("") ;
		return 0 ;
	}
	else if (choice == 'y' || choice == 'Y'){
        	skipLines(fd) ;
	        printLines(fd) ;
	}
	else{
		printCenteredString("Better hurry up before you catch a cold while staying here and        mindlessly staring at the revolving door.", 116) ;
		puts("") ;
		goto ENTRANCE_CHOICE ;
	}
	snowmanApproaches() ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printMessage() ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	if (fight("Snowman", 1, 100, 20, snowman_lines))
		return -1 ;
	levelUp() ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
INSIDE_CHOICE:
	printCenteredString("Which way are you going to pick? (t for TURNSTILE / e for ELEVATOR): ", 69) ;
	choice = readChar() ;
	if (choice == 't' || choice == 'T'){
		return 1 ;
	}
	else if (choice == 'e' || choice == 'E'){
		return 2 ;
	}
	else{
		printCenteredString("It's rather spooky here, better not stick around\n", 50) ;
		puts("") ;
		goto INSIDE_CHOICE ;
	}	
}

int8_t turnstileScene(FILE* fd){
	uint8_t choice ;
	puts("") ;
	printCenteredString("----------------------------------------------------------------------", 70) ;
	puts("\n\n") ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	accountantApproaches() ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	if (fight("Shop accountant", 3, 250, 30, accountant_lines))
		return -1 ;	
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	reindeerApproaches() ;
	printLines(fd) ;
	if (fight("Toy reindeer", 4, 300, 40, reindeer_lines))
		return -1 ;
	levelUp() ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printCenteredString("You've found a candy! Lucky you.\n", 33) ;	
	candies++ ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
TURNSTILE_CHOICE:
	printCenteredString("Which way are you going to pick? (e for ESCALATOR / d for DOOR): ", 69) ;
	choice = readChar() ;
	if (choice == 'e' || choice == 'E'){
		return 1 ;
	}
	else if (choice == 'd' || choice == 'D'){
		return 2 ;
	}
	else{
		printCenteredString("It's rather spooky here, better not stick around\n", 50) ;
		puts("") ;
		goto TURNSTILE_CHOICE ;
	}	
}

int8_t elevatorScene(FILE* fd){
	uint8_t choice ;
	puts("") ;
	printCenteredString("----------------------------------------------------------------------", 70) ;
	puts("\n\n") ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	trainApproaches() ;
	printLines(fd) ;
	if (fight("Christmas train", 3, 250, 30, train_lines))
		return -1 ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	conductorApproaches() ;
	printLines(fd) ;
	if (fight("Zombie conductor", 4, 300, 40, conductor_lines))
		return -1 ;
	levelUp() ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printCenteredString("You're thinking if you should examine the area. (y/n) ", 54) ;
	choice = readChar() ;
	if (choice == 'y' || choice == 'Y'){
		printLines(fd) ;
		printCenteredString("You've found a candy! Lucky you.\n", 33) ;	
		candies++ ;
		skipLines(fd) ;
	}
	else{
		skipLines(fd) ;
        	printLines(fd) ;
	}
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
ELEVATOR_CHOICE:
	printCenteredString("Which way are you going to pick? (e for ESCALATOR / d for DOOR): ", 69) ;
	choice = readChar() ;
	if (choice == 'e' || choice == 'E'){
		return 1 ;
	}
	else if (choice == 'd' || choice == 'D'){
		return 2 ;
	}
	else{
		printCenteredString("It's rather spooky here, better not stick around\n", 50) ;
		puts("") ;
		goto ELEVATOR_CHOICE ;
	}	
}

int8_t escalatorScene(FILE* fd){
	uint8_t choice ;
	puts("") ;
	printCenteredString("----------------------------------------------------------------------", 70) ;
	puts("\n\n") ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	elfApproaches() ;
	printCenteredString("\"Have you ever played a Christmas-themed dungeon crawl RPG before in your life?\" he asks, his eyes glimmering with hope. (y/n) ", 127) ;
	choice = readChar() ;
	if (choice == 'n' || choice == 'N'){
	        skipLines(fd) ;
	        skipLines(fd) ;
		printLines(fd) ;
		goto ESCALATOR_SKIP1 ;
	}
	else if (choice == 'y' || choice == 'Y'){
		printLines(fd) ;
	}
	else{
		printCenteredString("The elf's starting to lose his temper. It looks like the battle is    unavoidable now.\n", 120) ;
	        skipLines(fd) ;
	}
	printLines(fd) ;
	if (fight("Evil elf", 6, 450, 50, elf_lines))
		return -1 ;
	printCenteredString("The elf dropped a candy.\n", 26) ;	
	candies++ ;
	skipLines(fd) ;
ESCALATOR_SKIP1:
	sleep(STANDART_SLEEP_TIME) ;
	printCenteredString("\"Have you come here to endulge in a little Chrimas shopping then, some socks for your cousin and some useless candy for your little sister, perhaps?\" he wonders, looking directly at your face with a wicked     smirk. (y/n) ", 223) ;
	choice = readChar() ;
	if (choice == 'n' || choice == 'N'){
		skipLines(fd) ;
		skipLines(fd) ;
		skipLines(fd) ;
		printLines(fd) ;
		goto ESCALATOR_SKIP2 ;
	}
	else if (choice == 'y' || choice == 'Y'){
		printLines(fd) ;
	}
	else{
		printCenteredString("The elf's starting to lose his temper. It looks like the battle is    unavoidable now.\n", 120) ;
	        skipLines(fd) ;
	}
	printLines(fd) ;
	if (fight("Angry elf", 7, 600, 80, elf_lines))
		return -1 ;
	printLines(fd) ;
	skipLines(fd) ;
	printCenteredString("You pick up a bag of delicious candies!\n", 40) ;	
	candies += 3 ;
ESCALATOR_SKIP2:
	levelUp() ;
	return 0 ;
}

int8_t doorScene(FILE* fd){
	uint8_t choice ;
	puts("") ;
	printCenteredString("----------------------------------------------------------------------", 70) ;
	puts("\n\n") ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	giftboxApproaches() ;
	printLines(fd) ;
	if (fight("Evil giftbox", 6, 450, 50, giftbox_lines))
		return -1 ;
	sleep(STANDART_SLEEP_TIME) ;
	printCenteredString("You've found a candy! Lucky you.\n", 33) ;	
	candies++ ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
DOOR_CHOICE:
	printCenteredString("Are you willing to investigate? (y/n) ", 38) ;
	choice = readChar() ;
	if (choice == 'n' || choice == 'N'){
		skipLines(fd) ;
		skipLines(fd) ;
		printLines(fd) ;
	}
	else if (choice == 'y' || choice == 'Y'){
		printLines(fd) ;
		sleep(STANDART_SLEEP_TIME) ;
		mimicApproaches() ;
		printLines(fd) ;
		if (fight("Evil giftbox (mimic)", 7, 600, 80, mimic_lines))
			return -1 ;
		printCenteredString("Looking upon defeated giftbox, you witness a great wisdom, and now you get a double level up!\n", 94) ;
		levelUp() ;
		skipLines(fd) ;
	}
	else{
		printCenteredString("It's rather spooky here, better not stick around\n", 50) ;
		goto DOOR_CHOICE ;
	}
	levelUp() ;
	printLines(fd) ;
}

int8_t finalScene(FILE* fd){
	uint8_t choice ;
	puts("") ;
	printCenteredString("----------------------------------------------------------------------", 70) ;
	puts("\n\n") ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	treeApproaches() ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	if (fight("Xmas tree", 8, 800, 120, tree_lines))
		return -1 ;
	levelUp() ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	santaApproaches() ;
	printLines(fd) ;
	if (fight("Santa", 10, 1000, 180, santa_lines))
		return -1 ;
	levelUp() ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printLines(fd) ;
	sleep(STANDART_SLEEP_TIME) ;
	printCenteredString("G for GREEN, P for PURPLE: ", 27) ;
	choice = readChar() ;
	if (choice == 'p' || choice == 'P'){
		skipLines(fd) ;
		printLines(fd) ;
		printLines(fd) ;
		return 0 ;
	}
	else if (choice != 'g' && choice != 'G'){
		printCenteredString("You accidently smashed the green one\n", 37) ;
	}
	printLines(fd) ;
}

int main(int argc, char* argv[]){
	init() ;
	int8_t ret ;
	setvbuf(stdout, NULL, _IONBF, 0) ;
	FILE* fd = fopen("entrance.txt", "r") ;
	ret = firstScene(fd) ;
	switch (ret){
		case 0:
			return 0 ;
		case 1: 
			goto TURNSTILE ;
		case 2:
			goto ELEVATOR ;
		default:
			goto RIP ;
	}	
TURNSTILE:
	fd = fopen("turnstile.txt", "r") ;
	ret = turnstileScene(fd) ;
	switch (ret){
		case 1: 
			goto ESCALATOR ;
		case 2:
			goto DOOR ;
		default:
			goto RIP ;
	}
ELEVATOR:
	fd = fopen("elevator.txt", "r") ;
	ret = elevatorScene(fd) ;
	switch (ret){
		case 1: 
			goto ESCALATOR ;
		case 2:
			goto DOOR ;
		default:
			goto RIP ;
	}
ESCALATOR:
	fd = fopen("escalator.txt", "r") ;
	ret = escalatorScene(fd) ;
	if (ret == -1)
		goto RIP ;
	goto FINAL ;
DOOR:
	fd = fopen("door.txt", "r") ;
	if (ret == -1)
		goto RIP ;
	ret = doorScene(fd) ;
	goto FINAL ;
FINAL:
	fd = fopen("final.txt", "r") ;
	ret = finalScene(fd) ;
	if (ret == -1)
		goto RIP ;
	return 0 ;
RIP:
	rip() ;
}

