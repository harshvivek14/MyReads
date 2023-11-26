--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Homebrew)
-- Dumped by pg_dump version 14.9 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: read_books; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.read_books (
    id integer NOT NULL,
    user_id integer,
    book_id character varying NOT NULL
);


ALTER TABLE public.read_books OWNER TO postgres;

--
-- Name: read_books_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.read_books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.read_books_id_seq OWNER TO postgres;

--
-- Name: read_books_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.read_books_id_seq OWNED BY public.read_books.id;


--
-- Name: readlist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.readlist (
    id integer NOT NULL,
    name character varying(40) NOT NULL,
    user_id integer
);


ALTER TABLE public.readlist OWNER TO postgres;

--
-- Name: readlist_books; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.readlist_books (
    id integer NOT NULL,
    readlist_id integer,
    book_id character varying NOT NULL
);


ALTER TABLE public.readlist_books OWNER TO postgres;

--
-- Name: readlist_books_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.readlist_books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.readlist_books_id_seq OWNER TO postgres;

--
-- Name: readlist_books_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.readlist_books_id_seq OWNED BY public.readlist_books.id;


--
-- Name: readlist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.readlist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.readlist_id_seq OWNER TO postgres;

--
-- Name: readlist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.readlist_id_seq OWNED BY public.readlist.id;


--
-- Name: shared_readlist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shared_readlist (
    id integer NOT NULL,
    readlist_id integer,
    user_id integer,
    url_code character varying(20) NOT NULL
);


ALTER TABLE public.shared_readlist OWNER TO postgres;

--
-- Name: shared_readlist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shared_readlist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shared_readlist_id_seq OWNER TO postgres;

--
-- Name: shared_readlist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shared_readlist_id_seq OWNED BY public.shared_readlist.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    first_name character varying(35) NOT NULL,
    last_name character varying(35) NOT NULL,
    username character varying(15) NOT NULL,
    password text NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: read_books id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.read_books ALTER COLUMN id SET DEFAULT nextval('public.read_books_id_seq'::regclass);


--
-- Name: readlist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.readlist ALTER COLUMN id SET DEFAULT nextval('public.readlist_id_seq'::regclass);


--
-- Name: readlist_books id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.readlist_books ALTER COLUMN id SET DEFAULT nextval('public.readlist_books_id_seq'::regclass);


--
-- Name: shared_readlist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_readlist ALTER COLUMN id SET DEFAULT nextval('public.shared_readlist_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: read_books; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.read_books (id, user_id, book_id) FROM stdin;
29	2	K3KODwAAQBAJ
33	1	zAfSDwAAQBAJ
34	2	QTpzEAAAQBAJ
35	1	c3qmIZtWUjAC
36	1	gXlmAgAAQBAJ
\.


--
-- Data for Name: readlist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.readlist (id, name, user_id) FROM stdin;
10	list2	1
11	Assal Read List	2
12	Assal 2	2
13	final	1
\.


--
-- Data for Name: readlist_books; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.readlist_books (id, readlist_id, book_id) FROM stdin;
4	10	c3qmIZtWUjAC
6	10	zAfSDwAAQBAJ
7	11	JYsew1V4UTQC
8	11	QTpzEAAAQBAJ
\.


--
-- Data for Name: shared_readlist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shared_readlist (id, readlist_id, user_id, url_code) FROM stdin;
5	11	2	bMAkBUvkbN
6	13	1	cXDeOXDlei
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, first_name, last_name, username, password) FROM stdin;
1	hv	hv	hv	$2b$12$I7yraiHfvm4sQMUGRQR3nubM.nOdl1p1fzfiZ/GauXS0Hm3WCmucW
2	aa	aa	aa	$2b$12$yKe7hR/ymc8c5iFhvYZaJO3C38YMnDl7bxpJ20ike3XnEXsJHlx1W
\.


--
-- Name: read_books_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.read_books_id_seq', 36, true);


--
-- Name: readlist_books_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.readlist_books_id_seq', 9, true);


--
-- Name: readlist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.readlist_id_seq', 13, true);


--
-- Name: shared_readlist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shared_readlist_id_seq', 6, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 2, true);


--
-- Name: read_books read_books_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.read_books
    ADD CONSTRAINT read_books_pkey PRIMARY KEY (id);


--
-- Name: readlist_books readlist_books_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.readlist_books
    ADD CONSTRAINT readlist_books_pkey PRIMARY KEY (id);


--
-- Name: readlist readlist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.readlist
    ADD CONSTRAINT readlist_pkey PRIMARY KEY (id);


--
-- Name: shared_readlist shared_readlist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_readlist
    ADD CONSTRAINT shared_readlist_pkey PRIMARY KEY (id);


--
-- Name: shared_readlist shared_readlist_url_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_readlist
    ADD CONSTRAINT shared_readlist_url_code_key UNIQUE (url_code);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: read_books read_books_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.read_books
    ADD CONSTRAINT read_books_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: readlist readlist_author_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.readlist
    ADD CONSTRAINT readlist_author_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: readlist_books readlist_books_readlist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.readlist_books
    ADD CONSTRAINT readlist_books_readlist_id_fkey FOREIGN KEY (readlist_id) REFERENCES public.readlist(id) ON DELETE CASCADE;


--
-- Name: shared_readlist shared_readlist_readlist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_readlist
    ADD CONSTRAINT shared_readlist_readlist_id_fkey FOREIGN KEY (readlist_id) REFERENCES public.readlist(id) ON DELETE CASCADE;


--
-- Name: shared_readlist shared_readlist_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_readlist
    ADD CONSTRAINT shared_readlist_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

