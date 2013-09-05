drop table user_set_question;
drop table user_set;
drop table question_type_question;
drop table question;
drop table question_type;
drop table user_session;
drop table users;

create table users (
   id serial unique
 , username text not null unique
 , password text
 , firstname text
 , lastname text
 , nickname text
 , email text
);

create table user_session (
   id serial unique
 , user_id integer references users(id) on delete cascade on update cascade
 , cookie_sid text
 , login_time timestamp default now()
 , last_seen_time timestamp default now()
 , logged_in boolean not null default false
);

create table question_type (
   id serial unique
 , name text
 , level text
 , order_by float
 , expected_time text
 , expected_num_questions integer
);

create table question (
   id serial unique
 , question_html text
 , question_text text
 , correct_answer text
 , correct_answer2 text
 , correct_answer3 text
 , correct_answer4 text
);

create table question_type_question (
   id serial unique
 , question_type_id integer references question_type(id) on delete cascade on update cascade
 , question_id integer references question(id) on delete cascade on update cascade
);

create table user_set (
   id serial unique
 , user_id integer references users(id) on delete cascade on update cascade
 , question_type_id integer references question_type(id) on delete cascade on update cascade
 , num_questions integer
 , start_time timestamp default now()
 , end_time timestamp
 , all_correct boolean not null default false
);

create table user_set_question (
   id serial unique
 , user_set_id integer references user_set(id) on delete cascade on update cascade
 , question_num integer not null
 , question_id integer references question(id) on delete cascade on update cascade
 , start_time timestamp
 , end_time timestamp
 , answer text
 , answer2 text
 , answer3 text
 , answer4 text
 , answered_correctly boolean not null default false
);
create unique index user_set_question_user_set_id_question_num_idx on user_set_question(user_set_id, question_num);

insert into users (username, password, firstname, lastname, nickname, email) values 
  ('samortiz', '5c7447e4b552e04aef8fd9e8fc24b260d6a133cd316e69a655aec96757c60243', 'Sam', 'Ortiz', 'Sam', 'samortiz@gmail.com');
insert into users (username, password, firstname, lastname, nickname, email) values
  ('joyce', '4619d6b7c530dbfbf08431bfbd62484d1ccf296dda6c4e43d59d2027824539cd', 'Joyce', 'Ortiz', 'Joyce', 'joyce_oq@gmail.com');

