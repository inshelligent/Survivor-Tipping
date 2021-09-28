CREATE TABLE "contestants" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"age"	INTEGER,
	"occupation"	TEXT,
	"description"	TEXT,
	"is_eliminated"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE "tribals" (
	"tribal_date"	INTEGER NOT NULL,
	"voted_out"	INTEGER NOT NULL,
	PRIMARY KEY("tribal_date")
	FOREIGN KEY("voted_out") REFERENCES "contestants"("id"),
);
CREATE TABLE "users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"username"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"score"	INTEGER DEFAULT 0,
	PRIMARY KEY("id")
);
CREATE TABLE "votes" (
	"user_id"	INTEGER NOT NULL,
	"tribal_date"	NUMERIC NOT NULL,
	"first_choice_id"	INTEGER NOT NULL,
	"second_choice_id"	INTEGER,
	"third_choice_id"	INTEGER,
	PRIMARY KEY("user_id","tribal_date"),
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	FOREIGN KEY("first_choice_id") REFERENCES "contestants"("id"),
	FOREIGN KEY("second_choice_id") REFERENCES "contestants"("id"),
	FOREIGN KEY("third_choice_id") REFERENCES "contestants"("id")
);