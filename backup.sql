--
-- PostgreSQL database dump
--

\restrict VZzBYRXLe4aizIszSPCwmBr0skd1fVrFhRVLdDedrwpGmbqUupSBQofqD4i4Ge8

-- Dumped from database version 18.3 (Debian 18.3-1.pgdg12+1)
-- Dumped by pg_dump version 18.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

-- *not* creating schema, since initdb creates it


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    password character varying(200) NOT NULL
);


--
-- Name: admin_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.admin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: admin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.admin_id_seq OWNED BY public.admin.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: comment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    post_id integer NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    body text NOT NULL,
    date_posted timestamp without time zone,
    approved boolean DEFAULT false NOT NULL
);


--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: message; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.message (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    subject character varying(200) NOT NULL,
    message text NOT NULL,
    date_sent timestamp without time zone,
    is_read boolean
);


--
-- Name: message_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.message_id_seq OWNED BY public.message.id;


--
-- Name: podcast_episode; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.podcast_episode (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    description text,
    episode_number integer,
    audio_url character varying(500),
    spotify_url character varying(500),
    cover_image character varying(500),
    duration character varying(20),
    date_published timestamp without time zone,
    status character varying(20)
);


--
-- Name: podcast_episode_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.podcast_episode_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: podcast_episode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.podcast_episode_id_seq OWNED BY public.podcast_episode.id;


--
-- Name: post; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.post (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    slug character varying(200) NOT NULL,
    category character varying(80) NOT NULL,
    excerpt character varying(300) NOT NULL,
    content text NOT NULL,
    image character varying(500),
    date_posted timestamp without time zone,
    read_time character varying(20),
    status character varying(20) DEFAULT 'draft'::character varying,
    is_featured boolean DEFAULT false,
    tags character varying(200),
    scheduled_for timestamp without time zone,
    view_count integer DEFAULT 0 NOT NULL
);


--
-- Name: post_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.post_id_seq OWNED BY public.post.id;


--
-- Name: subscriber; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.subscriber (
    id integer NOT NULL,
    email character varying(150) NOT NULL,
    name character varying(100),
    date_subscribed timestamp without time zone,
    is_active boolean
);


--
-- Name: subscriber_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.subscriber_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: subscriber_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.subscriber_id_seq OWNED BY public.subscriber.id;


--
-- Name: admin id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin ALTER COLUMN id SET DEFAULT nextval('public.admin_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: message id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.message ALTER COLUMN id SET DEFAULT nextval('public.message_id_seq'::regclass);


--
-- Name: podcast_episode id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.podcast_episode ALTER COLUMN id SET DEFAULT nextval('public.podcast_episode_id_seq'::regclass);


--
-- Name: post id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post ALTER COLUMN id SET DEFAULT nextval('public.post_id_seq'::regclass);


--
-- Name: subscriber id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscriber ALTER COLUMN id SET DEFAULT nextval('public.subscriber_id_seq'::regclass);


--
-- Data for Name: admin; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.admin (id, username, password) FROM stdin;
1	ezinne	scrypt:32768:8:1$LLrhBbi3YxCjb9hr$a6488f3407d556702e663afc49fdd1b998009489f19ba023905f8af44482b6c6a629edb6cfa4acb8ce53c870d213f89b219a55e4fbe85ae30f74dce78b40b5e3
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
0f28bee38e6a
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.comment (id, post_id, name, email, body, date_posted, approved) FROM stdin;
2	1	Divine Nnata	divinennata@gmail.com	This is nice	2026-05-16 12:43:16.871947	t
1	4	Divine Nnata	divinennata@gmail.com	This is truly insightful	2026-05-16 12:39:26.524995	t
\.


--
-- Data for Name: message; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.message (id, name, email, subject, message, date_sent, is_read) FROM stdin;
\.


--
-- Data for Name: podcast_episode; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.podcast_episode (id, title, description, episode_number, audio_url, spotify_url, cover_image, duration, date_published, status) FROM stdin;
1	The Word made Flesh	"For as he thinks in his heart, so is he." (Proverbs 23:7)	1	\N	https://open.spotify.com/episode/4TGOftclT8D9bectcOmIKR	\N	14 mins	2026-05-16 14:42:21.675063	published
\.


--
-- Data for Name: post; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.post (id, title, slug, category, excerpt, content, image, date_posted, read_time, status, is_featured, tags, scheduled_for, view_count) FROM stdin;
1	The Unending Love of God	the-unending-love-of-god	Faith	A scriptural guide to discover God's unfathomable and unending love for you	<p>In a world filled with ups and downs, one thing remains constant - the love of God. It&#39;s a love that&#39;s unconditional, unending, and unwavering. A love that sees beyond our flaws and failures, and loves us anyway. &quot;For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.&quot; - John 3:16 God&#39;s love is not just a feeling, it&#39;s a choice. A choice to love us despite our imperfections, a choice to forgive us when we fall short, and a choice to redeem us from the pit of darkness. &quot;Love bears all things, believes all things, hopes all things, endures all things.&quot; - 1 Corinthians 13:7 In a world that&#39;s increasingly filled with hate, anger, and division, God&#39;s love stands as a beacon of hope. A reminder that we are loved, valued, and cherished - not for what we do, but for who we are. &quot;May you be strengthened with all power, according to his glorious might, for all endurance and patience with joy, giving thanks to the Father, who has qualified you to share in the inheritance of the saints in light.&quot; - Colossians 1:11-12 Let God&#39;s love be the anchor of your soul, the foundation of your life, and the hope that guides you through every storm. For in His love, we find our true purpose, our deepest joy, and our eternal peace. &quot;Who shall separate us from the love of Christ? Shall trouble or hardship or persecution or famine or nakedness or danger or sword?... No, in all these things we are more than conquerors through him who loved us.&quot; - Romans 8:35-37.</p>\r\n	https://res.cloudinary.com/dwdx6e8gi/image/upload/v1778713989/gq9hlkvnhlnkpatajtqm.jpg	2026-05-04 15:24:18.281049	5 mins read	published	f		\N	0
4	5 Signs You Are Healing (Even When It Doesn't Feel Like It)	5-signs-you-are-healing-even-when-it-doesn-t-feel-like-it	Healing	Healing rarely announces itself. It doesn't arrive with a dramatic moment or a sudden feeling of wholeness. Most of the time, it is quiet, slow, and easy to miss — until you look back.	<p><img alt="" src="https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=1200&amp;q=80" />Nobody warns you that healing is quiet. You expect a moment &mdash; a morning you wake up and the weight is simply gone, a conversation that finally closes the wound, a prayer that lands and everything shifts. But healing rarely works like that.</p>\r\n\r\n<p>More often, it sneaks up on you. You look back three months later and realize the thing that used to destroy you now only stings. That is not nothing. That is everything.</p>\r\n\r\n<p>Here are five signs that you are healing, even on the days it does not feel that way.</p>\r\n\r\n<h2>1. You Can Talk About It Without Falling Apart</h2>\r\n\r\n<p>There was a time when saying their name, or describing what happened, would send you spiralling. Now you can say it &mdash; maybe not perfectly, maybe with a tremor in your voice &mdash; but you can say it and remain standing. That distance between you and the pain is healing doing its quiet work.</p>\r\n\r\n<h2>2. Your Triggers Are Getting Smaller</h2>\r\n\r\n<p>Healing does not mean you will never be triggered. It means the triggers shrink. The song that once ruined your whole day now only takes a few minutes to shake off. The situation that sent you into panic now makes you pause instead of collapse. Smaller reactions are signs of a nervous system learning it is safe again.</p>\r\n\r\n<h2>3. You Are Choosing Yourself More</h2>\r\n\r\n<p>You said no to something that would have depleted you. You left a conversation that was going nowhere. You chose rest over people-pleasing. These are not small things. Broken people shrink themselves to survive. Healing people begin to take up the space they were always meant to occupy.</p>\r\n\r\n<h2>4. You Feel Anger Instead of Just Sadness</h2>\r\n\r\n<p>This might surprise you, but anger is often a sign of progress. Sadness keeps us small and turned inward. Anger &mdash; healthy, directed anger &mdash; is the part of us that knows we deserved better. If you have moved from grief to a quiet fire, that fire is your dignity returning.</p>\r\n\r\n<h2>5. You Can Imagine a Future</h2>\r\n\r\n<p>At your lowest, the future felt like a blank wall. Nothing beyond today. Healing restores your imagination. You start making small plans. You allow yourself to want things again. You think, <em>maybe one day</em> &mdash; and you actually mean it.</p>\r\n\r\n<h2>Give Yourself Credit</h2>\r\n\r\n<p>Healing is not linear, and it is not loud. Some days you will feel like you are back at the beginning, and that is okay. The setback is not the truth &mdash; the overall direction is. And the overall direction is <strong>forward</strong>.</p>\r\n\r\n<p>You are doing better than you think. Keep going.</p>\r\n	\N	2026-05-13 23:18:36.05776	5 min read	published	f		\N	0
3	When Prayer Feels Like Talking to the Ceiling	when-prayer-feels-like-talking-to-the-ceiling	Faith	Have you ever prayed and felt absolutely nothing? No warmth, no answer, no sign — just your own voice bouncing back at you. You are not alone, and your faith is not broken.	<p>There are seasons in life when prayer feels like the loneliest act you can perform. You close your eyes, you fold your hands, you speak &mdash; and the silence on the other end feels deafening. No warmth. No peace. No sign. Just you, and the ceiling, and a quiet that feels more like absence than rest.</p>\r\n\r\n<p>If that is where you are right now, I need you to hear this first: <strong>your faith is not broken</strong>. Dry seasons are not punishment. They are part of the journey.</p>\r\n\r\n<h2>Why God Can Feel Distant</h2>\r\n\r\n<p>The Psalms are full of this tension. David &mdash; a man called after God&#39;s own heart &mdash; wrote words like <em>&quot;My God, my God, why have you forsaken me?&quot;</em> (Psalm 22:1). If the most celebrated worshipper in Scripture felt abandoned, you are in very good company.</p>\r\n\r\n<p>Distance in prayer is rarely about God moving away. More often it is about:</p>\r\n\r\n<ul>\r\n\t<li><strong>Exhaustion</strong> &mdash; When you are running on empty emotionally, everything feels numb, including your spiritual life.</li>\r\n\t<li><strong>Unprocessed pain</strong> &mdash; Grief, disappointment, and anger can build a wall between us and vulnerability &mdash; even with God.</li>\r\n\t<li><strong>Expectation mismatch</strong> &mdash; We expect prayer to feel a certain way, and when it does not, we assume something is wrong.</li>\r\n</ul>\r\n\r\n<h2>What To Do When the Words Won&#39;t Come</h2>\r\n\r\n<p>Sometimes the most honest prayer is the shortest one. <em>&quot;I don&#39;t know how to talk to you right now, but I&#39;m here.&quot;</em> That is enough. God is not grading your eloquence. He is responding to your heart.</p>\r\n\r\n<p>Try these when you feel stuck:</p>\r\n\r\n<ul>\r\n\t<li><strong>Pray the Psalms out loud.</strong> Let someone else&#39;s words carry you until yours return.</li>\r\n\t<li><strong>Sit in silence without agenda.</strong> Not every prayer needs to be a request. Sometimes showing up is the prayer.</li>\r\n\t<li><strong>Write it down.</strong> Journaling your prayers removes the pressure of performing and makes space for honesty.</li>\r\n\t<li><strong>Tell God exactly how you feel.</strong> Including the doubt. Including the frustration. He can handle it.</li>\r\n</ul>\r\n\r\n<h2>The Ceiling is Not the End</h2>\r\n\r\n<p>Every person who has walked deeply with God has passed through a dry valley. The valley is not where the story ends &mdash; it is where character is built, where desperation strips away performance, and where a more authentic faith is forged.</p>\r\n\r\n<p>Keep showing up. Keep whispering. The silence is not rejection. Sometimes it is simply an invitation to go deeper than words.</p>\r\n\r\n<p><em>You are not forgotten. You are not too far gone. And that ceiling? It has never once stopped a single prayer.</em></p>\r\n	https://res.cloudinary.com/dwdx6e8gi/image/upload/v1778714162/hnwa9itvnpgxbtuozkel.png	2026-05-13 23:16:03.394282	4 min read	published	f		\N	0
5	Am I actually healing? 	am-i-actually-healing	Healing	Healing rarely announces itself. It doesn't arrive with a dramatic moment or a sudden feeling of wholeness. Most of the time, it is quiet, slow, and easy to miss — until you look back.	<p><img alt="" src="https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=1200&amp;q=80" style="height:800px; width:1200px" />Nobody warns you that healing is quiet. You expect a moment &mdash; a morning you wake up and the weight is simply gone, a conversation that finally closes the wound, a prayer that lands and everything shifts. But healing rarely works like that.</p>\r\n\r\n<p>More often, it sneaks up on you. You look back three months later and realize the thing that used to destroy you now only stings. That is not nothing. That is everything.</p>\r\n\r\n<p>Here are five signs that you are healing, even on the days it does not feel that way.</p>\r\n\r\n<h2>1. You Can Talk About It Without Falling Apart</h2>\r\n\r\n<p>There was a time when saying their name, or describing what happened, would send you spiralling. Now you can say it &mdash; maybe not perfectly, maybe with a tremor in your voice &mdash; but you can say it and remain standing. That distance between you and the pain is healing doing its quiet work.</p>\r\n\r\n<h2>2. Your Triggers Are Getting Smaller</h2>\r\n\r\n<p>Healing does not mean you will never be triggered. It means the triggers shrink. The song that once ruined your whole day now only takes a few minutes to shake off. The situation that sent you into panic now makes you pause instead of collapse. Smaller reactions are signs of a nervous system learning it is safe again.</p>\r\n\r\n<h2>3. You Are Choosing Yourself More</h2>\r\n\r\n<p>You said no to something that would have depleted you. You left a conversation that was going nowhere. You chose rest over people-pleasing. These are not small things. Broken people shrink themselves to survive. Healing people begin to take up the space they were always meant to occupy.</p>\r\n\r\n<h2>4. You Feel Anger Instead of Just Sadness</h2>\r\n\r\n<p>This might surprise you, but anger is often a sign of progress. Sadness keeps us small and turned inward. Anger &mdash; healthy, directed anger &mdash; is the part of us that knows we deserved better. If you have moved from grief to a quiet fire, that fire is your dignity returning.</p>\r\n\r\n<h2>5. You Can Imagine a Future</h2>\r\n\r\n<p>At your lowest, the future felt like a blank wall. Nothing beyond today. Healing restores your imagination. You start making small plans. You allow yourself to want things again. You think, <em>maybe one day</em> &mdash; and you actually mean it.</p>\r\n\r\n<h2>Give Yourself Credit</h2>\r\n\r\n<p>Healing is not linear, and it is not loud. Some days you will feel like you are back at the beginning, and that is okay. The setback is not the truth &mdash; the overall direction is. And the overall direction is <strong>forward</strong>.</p>\r\n\r\n<p>You are doing better than you think. Keep going.</p>\r\n	\N	2026-05-13 23:19:45.803278	5 min read	published	f		\N	0
\.


--
-- Data for Name: subscriber; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.subscriber (id, email, name, date_subscribed, is_active) FROM stdin;
1	obasinneoma346@gmail.com	Mercy	2026-05-16 10:45:00.073366	t
\.


--
-- Name: admin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.admin_id_seq', 1, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.comment_id_seq', 2, true);


--
-- Name: message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.message_id_seq', 1, false);


--
-- Name: podcast_episode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.podcast_episode_id_seq', 1, true);


--
-- Name: post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.post_id_seq', 5, true);


--
-- Name: subscriber_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.subscriber_id_seq', 1, true);


--
-- Name: admin admin_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (id);


--
-- Name: admin admin_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_username_key UNIQUE (username);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: comment comment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_pkey PRIMARY KEY (id);


--
-- Name: message message_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- Name: podcast_episode podcast_episode_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.podcast_episode
    ADD CONSTRAINT podcast_episode_pkey PRIMARY KEY (id);


--
-- Name: post post_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_pkey PRIMARY KEY (id);


--
-- Name: post post_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_slug_key UNIQUE (slug);


--
-- Name: subscriber subscriber_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscriber
    ADD CONSTRAINT subscriber_email_key UNIQUE (email);


--
-- Name: subscriber subscriber_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscriber
    ADD CONSTRAINT subscriber_pkey PRIMARY KEY (id);


--
-- Name: comment comment_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.post(id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: -; Owner: -
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON SEQUENCES TO innerpeace_hub_user;


--
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: -; Owner: -
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TYPES TO innerpeace_hub_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: -; Owner: -
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS TO innerpeace_hub_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: -
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES TO innerpeace_hub_user;


--
-- PostgreSQL database dump complete
--

\unrestrict VZzBYRXLe4aizIszSPCwmBr0skd1fVrFhRVLdDedrwpGmbqUupSBQofqD4i4Ge8

