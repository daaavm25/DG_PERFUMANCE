--
-- PostgreSQL database dump
--

\restrict VOhHswMp1LEKRJY1GW2zekA9SH0lTKwaBZRXzrpefFcr2F6vEBLQEtGOHr0e2Bo

-- Dumped from database version 17.6 (Debian 17.6-0+deb13u1)
-- Dumped by pg_dump version 17.6 (Debian 17.6-0+deb13u1)

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
-- Name: gestion_perfumance; Type: SCHEMA; Schema: -; Owner: admin_perfumance
--

CREATE SCHEMA gestion_perfumance;


ALTER SCHEMA gestion_perfumance OWNER TO admin_perfumance;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cliente; Type: TABLE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE TABLE gestion_perfumance.cliente (
    id_cliente integer NOT NULL,
    nombres character varying(50) NOT NULL,
    apellidos character varying(100) NOT NULL,
    telefono character varying(20),
    email character varying(100)
);


ALTER TABLE gestion_perfumance.cliente OWNER TO admin_perfumance;

--
-- Name: cliente_id_cliente_seq; Type: SEQUENCE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE SEQUENCE gestion_perfumance.cliente_id_cliente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE gestion_perfumance.cliente_id_cliente_seq OWNER TO admin_perfumance;

--
-- Name: cliente_id_cliente_seq; Type: SEQUENCE OWNED BY; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER SEQUENCE gestion_perfumance.cliente_id_cliente_seq OWNED BY gestion_perfumance.cliente.id_cliente;


--
-- Name: compra; Type: TABLE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE TABLE gestion_perfumance.compra (
    id_compra integer NOT NULL,
    fecha_compra timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    costo_total numeric(10,2) NOT NULL,
    id_proveedor integer NOT NULL
);


ALTER TABLE gestion_perfumance.compra OWNER TO admin_perfumance;

--
-- Name: compra_id_compra_seq; Type: SEQUENCE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE SEQUENCE gestion_perfumance.compra_id_compra_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE gestion_perfumance.compra_id_compra_seq OWNER TO admin_perfumance;

--
-- Name: compra_id_compra_seq; Type: SEQUENCE OWNED BY; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER SEQUENCE gestion_perfumance.compra_id_compra_seq OWNED BY gestion_perfumance.compra.id_compra;


--
-- Name: detalle_compra; Type: TABLE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE TABLE gestion_perfumance.detalle_compra (
    id_detalle_compra integer NOT NULL,
    id_compra integer NOT NULL,
    id_perfume integer NOT NULL,
    cantidad integer NOT NULL,
    costo_unitario numeric(10,2) NOT NULL
);


ALTER TABLE gestion_perfumance.detalle_compra OWNER TO admin_perfumance;

--
-- Name: detalle_compra_id_detalle_compra_seq; Type: SEQUENCE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE SEQUENCE gestion_perfumance.detalle_compra_id_detalle_compra_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE gestion_perfumance.detalle_compra_id_detalle_compra_seq OWNER TO admin_perfumance;

--
-- Name: detalle_compra_id_detalle_compra_seq; Type: SEQUENCE OWNED BY; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER SEQUENCE gestion_perfumance.detalle_compra_id_detalle_compra_seq OWNED BY gestion_perfumance.detalle_compra.id_detalle_compra;


--
-- Name: detalle_venta; Type: TABLE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE TABLE gestion_perfumance.detalle_venta (
    id_detalle_venta integer NOT NULL,
    id_venta integer NOT NULL,
    id_perfume integer NOT NULL,
    cantidad integer NOT NULL,
    precio_unitario numeric(10,2) NOT NULL
);


ALTER TABLE gestion_perfumance.detalle_venta OWNER TO admin_perfumance;

--
-- Name: detalle_venta_id_detalle_venta_seq; Type: SEQUENCE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE SEQUENCE gestion_perfumance.detalle_venta_id_detalle_venta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE gestion_perfumance.detalle_venta_id_detalle_venta_seq OWNER TO admin_perfumance;

--
-- Name: detalle_venta_id_detalle_venta_seq; Type: SEQUENCE OWNED BY; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER SEQUENCE gestion_perfumance.detalle_venta_id_detalle_venta_seq OWNED BY gestion_perfumance.detalle_venta.id_detalle_venta;


--
-- Name: empleado; Type: TABLE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE TABLE gestion_perfumance.empleado (
    id_empleado integer NOT NULL,
    nombres character varying(50) NOT NULL,
    apellidos character varying(50) NOT NULL,
    telefono character varying(20),
    email character varying(100),
    id_rol integer
);


ALTER TABLE gestion_perfumance.empleado OWNER TO admin_perfumance;

--
-- Name: empleado_id_empleado_seq; Type: SEQUENCE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE SEQUENCE gestion_perfumance.empleado_id_empleado_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE gestion_perfumance.empleado_id_empleado_seq OWNER TO admin_perfumance;

--
-- Name: empleado_id_empleado_seq; Type: SEQUENCE OWNED BY; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER SEQUENCE gestion_perfumance.empleado_id_empleado_seq OWNED BY gestion_perfumance.empleado.id_empleado;


--
-- Name: genero; Type: TABLE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE TABLE gestion_perfumance.genero (
    id_genero integer NOT NULL,
    descripcion character varying(30) NOT NULL
);


ALTER TABLE gestion_perfumance.genero OWNER TO admin_perfumance;

--
-- Name: genero_id_genero_seq; Type: SEQUENCE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE SEQUENCE gestion_perfumance.genero_id_genero_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE gestion_perfumance.genero_id_genero_seq OWNER TO admin_perfumance;

--
-- Name: genero_id_genero_seq; Type: SEQUENCE OWNED BY; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER SEQUENCE gestion_perfumance.genero_id_genero_seq OWNED BY gestion_perfumance.genero.id_genero;


--
-- Name: perfume; Type: TABLE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE TABLE gestion_perfumance.perfume (
    id_perfume integer NOT NULL,
    marca character varying(50) NOT NULL,
    presentacion character varying(50),
    talla character varying(20),
    id_genero integer NOT NULL,
    stock integer DEFAULT 0,
    fecha_caducidad date
);


ALTER TABLE gestion_perfumance.perfume OWNER TO admin_perfumance;

--
-- Name: perfume_id_perfume_seq; Type: SEQUENCE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE SEQUENCE gestion_perfumance.perfume_id_perfume_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE gestion_perfumance.perfume_id_perfume_seq OWNER TO admin_perfumance;

--
-- Name: perfume_id_perfume_seq; Type: SEQUENCE OWNED BY; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER SEQUENCE gestion_perfumance.perfume_id_perfume_seq OWNED BY gestion_perfumance.perfume.id_perfume;


--
-- Name: proveedor; Type: TABLE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE TABLE gestion_perfumance.proveedor (
    id_proveedor integer NOT NULL,
    nombre character varying(100) NOT NULL,
    telefono character varying(20),
    email character varying(100),
    direccion character varying(200),
    condiciones_comerciales text
);


ALTER TABLE gestion_perfumance.proveedor OWNER TO admin_perfumance;

--
-- Name: proveedor_id_proveedor_seq; Type: SEQUENCE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE SEQUENCE gestion_perfumance.proveedor_id_proveedor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE gestion_perfumance.proveedor_id_proveedor_seq OWNER TO admin_perfumance;

--
-- Name: proveedor_id_proveedor_seq; Type: SEQUENCE OWNED BY; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER SEQUENCE gestion_perfumance.proveedor_id_proveedor_seq OWNED BY gestion_perfumance.proveedor.id_proveedor;


--
-- Name: rol; Type: TABLE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE TABLE gestion_perfumance.rol (
    id_rol integer NOT NULL,
    descripcion character varying(50) NOT NULL
);


ALTER TABLE gestion_perfumance.rol OWNER TO admin_perfumance;

--
-- Name: rol_id_rol_seq; Type: SEQUENCE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE SEQUENCE gestion_perfumance.rol_id_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE gestion_perfumance.rol_id_rol_seq OWNER TO admin_perfumance;

--
-- Name: rol_id_rol_seq; Type: SEQUENCE OWNED BY; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER SEQUENCE gestion_perfumance.rol_id_rol_seq OWNED BY gestion_perfumance.rol.id_rol;


--
-- Name: usuario; Type: TABLE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE TABLE gestion_perfumance.usuario (
    id_usuario integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(200) NOT NULL,
    email character varying(100),
    id_rol integer NOT NULL,
    activo boolean DEFAULT true,
    id_cliente integer,
    id_empleado integer
);


ALTER TABLE gestion_perfumance.usuario OWNER TO admin_perfumance;

--
-- Name: usuario_id_usuario_seq; Type: SEQUENCE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE SEQUENCE gestion_perfumance.usuario_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE gestion_perfumance.usuario_id_usuario_seq OWNER TO admin_perfumance;

--
-- Name: usuario_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER SEQUENCE gestion_perfumance.usuario_id_usuario_seq OWNED BY gestion_perfumance.usuario.id_usuario;


--
-- Name: venta; Type: TABLE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE TABLE gestion_perfumance.venta (
    id_venta integer NOT NULL,
    fecha_venta timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    monto_total numeric(10,2) NOT NULL,
    id_cliente integer NOT NULL,
    id_empleado integer
);


ALTER TABLE gestion_perfumance.venta OWNER TO admin_perfumance;

--
-- Name: venta_id_venta_seq; Type: SEQUENCE; Schema: gestion_perfumance; Owner: admin_perfumance
--

CREATE SEQUENCE gestion_perfumance.venta_id_venta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE gestion_perfumance.venta_id_venta_seq OWNER TO admin_perfumance;

--
-- Name: venta_id_venta_seq; Type: SEQUENCE OWNED BY; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER SEQUENCE gestion_perfumance.venta_id_venta_seq OWNED BY gestion_perfumance.venta.id_venta;


--
-- Name: cliente id_cliente; Type: DEFAULT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.cliente ALTER COLUMN id_cliente SET DEFAULT nextval('gestion_perfumance.cliente_id_cliente_seq'::regclass);


--
-- Name: compra id_compra; Type: DEFAULT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.compra ALTER COLUMN id_compra SET DEFAULT nextval('gestion_perfumance.compra_id_compra_seq'::regclass);


--
-- Name: detalle_compra id_detalle_compra; Type: DEFAULT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.detalle_compra ALTER COLUMN id_detalle_compra SET DEFAULT nextval('gestion_perfumance.detalle_compra_id_detalle_compra_seq'::regclass);


--
-- Name: detalle_venta id_detalle_venta; Type: DEFAULT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.detalle_venta ALTER COLUMN id_detalle_venta SET DEFAULT nextval('gestion_perfumance.detalle_venta_id_detalle_venta_seq'::regclass);


--
-- Name: empleado id_empleado; Type: DEFAULT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.empleado ALTER COLUMN id_empleado SET DEFAULT nextval('gestion_perfumance.empleado_id_empleado_seq'::regclass);


--
-- Name: genero id_genero; Type: DEFAULT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.genero ALTER COLUMN id_genero SET DEFAULT nextval('gestion_perfumance.genero_id_genero_seq'::regclass);


--
-- Name: perfume id_perfume; Type: DEFAULT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.perfume ALTER COLUMN id_perfume SET DEFAULT nextval('gestion_perfumance.perfume_id_perfume_seq'::regclass);


--
-- Name: proveedor id_proveedor; Type: DEFAULT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.proveedor ALTER COLUMN id_proveedor SET DEFAULT nextval('gestion_perfumance.proveedor_id_proveedor_seq'::regclass);


--
-- Name: rol id_rol; Type: DEFAULT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.rol ALTER COLUMN id_rol SET DEFAULT nextval('gestion_perfumance.rol_id_rol_seq'::regclass);


--
-- Name: usuario id_usuario; Type: DEFAULT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.usuario ALTER COLUMN id_usuario SET DEFAULT nextval('gestion_perfumance.usuario_id_usuario_seq'::regclass);


--
-- Name: venta id_venta; Type: DEFAULT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.venta ALTER COLUMN id_venta SET DEFAULT nextval('gestion_perfumance.venta_id_venta_seq'::regclass);


--
-- Name: cliente cliente_email_key; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.cliente
    ADD CONSTRAINT cliente_email_key UNIQUE (email);


--
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id_cliente);


--
-- Name: compra compra_pkey; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.compra
    ADD CONSTRAINT compra_pkey PRIMARY KEY (id_compra);


--
-- Name: detalle_compra detalle_compra_pkey; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.detalle_compra
    ADD CONSTRAINT detalle_compra_pkey PRIMARY KEY (id_detalle_compra);


--
-- Name: detalle_venta detalle_venta_pkey; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.detalle_venta
    ADD CONSTRAINT detalle_venta_pkey PRIMARY KEY (id_detalle_venta);


--
-- Name: empleado empleado_email_key; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.empleado
    ADD CONSTRAINT empleado_email_key UNIQUE (email);


--
-- Name: empleado empleado_pkey; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.empleado
    ADD CONSTRAINT empleado_pkey PRIMARY KEY (id_empleado);


--
-- Name: genero genero_descripcion_key; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.genero
    ADD CONSTRAINT genero_descripcion_key UNIQUE (descripcion);


--
-- Name: genero genero_pkey; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.genero
    ADD CONSTRAINT genero_pkey PRIMARY KEY (id_genero);


--
-- Name: perfume perfume_pkey; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.perfume
    ADD CONSTRAINT perfume_pkey PRIMARY KEY (id_perfume);


--
-- Name: proveedor proveedor_pkey; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.proveedor
    ADD CONSTRAINT proveedor_pkey PRIMARY KEY (id_proveedor);


--
-- Name: rol rol_descripcion_key; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.rol
    ADD CONSTRAINT rol_descripcion_key UNIQUE (descripcion);


--
-- Name: rol rol_pkey; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (id_rol);


--
-- Name: usuario usuario_email_key; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.usuario
    ADD CONSTRAINT usuario_email_key UNIQUE (email);


--
-- Name: usuario usuario_id_cliente_key; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.usuario
    ADD CONSTRAINT usuario_id_cliente_key UNIQUE (id_cliente);


--
-- Name: usuario usuario_id_empleado_key; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.usuario
    ADD CONSTRAINT usuario_id_empleado_key UNIQUE (id_empleado);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario);


--
-- Name: usuario usuario_username_key; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.usuario
    ADD CONSTRAINT usuario_username_key UNIQUE (username);


--
-- Name: venta venta_pkey; Type: CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.venta
    ADD CONSTRAINT venta_pkey PRIMARY KEY (id_venta);


--
-- Name: compra compra_id_proveedor_fkey; Type: FK CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.compra
    ADD CONSTRAINT compra_id_proveedor_fkey FOREIGN KEY (id_proveedor) REFERENCES gestion_perfumance.proveedor(id_proveedor);


--
-- Name: detalle_compra detalle_compra_id_compra_fkey; Type: FK CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.detalle_compra
    ADD CONSTRAINT detalle_compra_id_compra_fkey FOREIGN KEY (id_compra) REFERENCES gestion_perfumance.compra(id_compra);


--
-- Name: detalle_compra detalle_compra_id_perfume_fkey; Type: FK CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.detalle_compra
    ADD CONSTRAINT detalle_compra_id_perfume_fkey FOREIGN KEY (id_perfume) REFERENCES gestion_perfumance.perfume(id_perfume);


--
-- Name: detalle_venta detalle_venta_id_perfume_fkey; Type: FK CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.detalle_venta
    ADD CONSTRAINT detalle_venta_id_perfume_fkey FOREIGN KEY (id_perfume) REFERENCES gestion_perfumance.perfume(id_perfume);


--
-- Name: detalle_venta detalle_venta_id_venta_fkey; Type: FK CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.detalle_venta
    ADD CONSTRAINT detalle_venta_id_venta_fkey FOREIGN KEY (id_venta) REFERENCES gestion_perfumance.venta(id_venta) ON DELETE CASCADE;


--
-- Name: empleado empleado_id_rol_fkey; Type: FK CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.empleado
    ADD CONSTRAINT empleado_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES gestion_perfumance.rol(id_rol);


--
-- Name: perfume perfume_id_genero_fkey; Type: FK CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.perfume
    ADD CONSTRAINT perfume_id_genero_fkey FOREIGN KEY (id_genero) REFERENCES gestion_perfumance.genero(id_genero);


--
-- Name: usuario usuario_id_cliente_fkey; Type: FK CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.usuario
    ADD CONSTRAINT usuario_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES gestion_perfumance.cliente(id_cliente);


--
-- Name: usuario usuario_id_empleado_fkey; Type: FK CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.usuario
    ADD CONSTRAINT usuario_id_empleado_fkey FOREIGN KEY (id_empleado) REFERENCES gestion_perfumance.empleado(id_empleado);


--
-- Name: usuario usuario_id_rol_fkey; Type: FK CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.usuario
    ADD CONSTRAINT usuario_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES gestion_perfumance.rol(id_rol);


--
-- Name: venta venta_id_cliente_fkey; Type: FK CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.venta
    ADD CONSTRAINT venta_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES gestion_perfumance.cliente(id_cliente);


--
-- Name: venta venta_id_empleado_fkey; Type: FK CONSTRAINT; Schema: gestion_perfumance; Owner: admin_perfumance
--

ALTER TABLE ONLY gestion_perfumance.venta
    ADD CONSTRAINT venta_id_empleado_fkey FOREIGN KEY (id_empleado) REFERENCES gestion_perfumance.empleado(id_empleado);


--
-- PostgreSQL database dump complete
--

\unrestrict VOhHswMp1LEKRJY1GW2zekA9SH0lTKwaBZRXzrpefFcr2F6vEBLQEtGOHr0e2Bo
