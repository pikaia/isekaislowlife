import psycopg2

from slowlife.db.config import load_config


def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS slowlife.fish_encyclopedia (
            name text NOT NULL DEFAULT '',
            amount INTEGER NOT NULL DEFAULT 0,
            longest float NOT NULL DEFAULT 0.0,
            base_level INTEGER NOT NULL DEFAULT 0,
            base_buff text NOT NULL DEFAULT '',
            crowned_level INTEGER NOT NULL DEFAULT 0,
            crowned_buff text NOT NULL DEFAULT '',
            last_update timestamp NOT NULL DEFAULT now()
        );
        ALTER TABLE IF EXISTS slowlife.fish_encyclopedia
            OWNER to pik;        
        """,
        """ CREATE TABLE IF NOT EXISTS slowlife.antique_encyclopedia (
                name text PRIMARY KEY,
                description text NOT NULL DEFAULT '',
                first_obtained timestamp,
                level INTEGER NOT  NULL DEFAULT 0,
                buff text NOT NULL DEFAULT '',
                last_update timestamp NOT NULL DEFAULT now()
            );
        ALTER TABLE IF EXISTS slowlife.antique_encyclopedia
            OWNER to pik;        
        """,
        """ CREATE TABLE IF NOT EXISTS slowlife.combination_encyclopedia (
                name text PRIMARY KEY,
                description text NOT NULL DEFAULT '',
                completion_in timestamp,
                base_buff text,
                combination_buff text,
                last_update timestamp NOT NULL DEFAULT now()
            );
        ALTER TABLE IF EXISTS slowlife.combination_encyclopedia
            OWNER to pik;
        """,
        """ CREATE TABLE IF NOT EXISTS slowlife.player (
                id bigint NOT NULL,
                name text COLLATE pg_catalog."default" NOT NULL,
                server text COLLATE pg_catalog."default",
                guild text COLLATE pg_catalog."default",
                last_update timestamp with time zone NOT NULL,
                CONSTRAINT player_pkey PRIMARY KEY (id)
            );
        ALTER TABLE IF EXISTS slowlife.player
            OWNER to pik;
        """,
        """ CREATE TABLE IF NOT EXISTS slowlife.guild (
                id bigint NOT NULL,
                name text COLLATE pg_catalog."default" NOT NULL,
                num_members integer,
                max_members integer,
                last_update timestamp with time zone NOT NULL,
                CONSTRAINT guild_pkey PRIMARY KEY (id)
            );
        ALTER TABLE IF EXISTS slowlife.guild
            OWNER to pik;
        """)

    try:
        config = load_config()
        print(f'DB config: {config}')
        with psycopg2.connect(**config) as conn:
            print(f'DB connection: {conn}')
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                for command in commands:
                    res = cur.execute(command)
                    print(res)
                    cur.execute('COMMIT')
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    create_tables()
