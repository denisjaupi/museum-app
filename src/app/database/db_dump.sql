PGDMP  
    .            
    |            museum_app_db    16.2    16.2 '    0           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            1           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            2           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            3           1262    17290    museum_app_db    DATABASE     o   CREATE DATABASE museum_app_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
    DROP DATABASE museum_app_db;
                postgres    false            �            1255    17300    set_immagine_id()    FUNCTION     �   CREATE FUNCTION public.set_immagine_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.immagine_id := (
        SELECT COALESCE(MAX(immagine_id), 0) + 1
        FROM opere_d_arte
        WHERE id = NEW.id
    );
    RETURN NEW;
END;
$$;
 (   DROP FUNCTION public.set_immagine_id();
       public          postgres    false            �            1259    17292    opere_d_arte    TABLE     �   CREATE TABLE public.opere_d_arte (
    id integer NOT NULL,
    immagine_id integer NOT NULL,
    titolo jsonb,
    autore text,
    descrizione jsonb,
    percorso_immagine text,
    sottotitolo text
);
     DROP TABLE public.opere_d_arte;
       public         heap    postgres    false            �            1259    17291    artworks_immagine_id_seq    SEQUENCE     �   CREATE SEQUENCE public.artworks_immagine_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.artworks_immagine_id_seq;
       public          postgres    false    216            4           0    0    artworks_immagine_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.artworks_immagine_id_seq OWNED BY public.opere_d_arte.immagine_id;
          public          postgres    false    215            �            1259    17303    dettagli_opera    TABLE     �   CREATE TABLE public.dettagli_opera (
    id_dettaglio integer NOT NULL,
    id integer,
    immagine_id integer,
    titolo jsonb,
    testo jsonb,
    coordinata_x double precision,
    coordinata_y double precision
);
 "   DROP TABLE public.dettagli_opera;
       public         heap    postgres    false            �            1259    17302    dettagli_opera_id_dettaglio_seq    SEQUENCE     �   CREATE SEQUENCE public.dettagli_opera_id_dettaglio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.dettagli_opera_id_dettaglio_seq;
       public          postgres    false    218            5           0    0    dettagli_opera_id_dettaglio_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.dettagli_opera_id_dettaglio_seq OWNED BY public.dettagli_opera.id_dettaglio;
          public          postgres    false    217            �            1259    17328    lingue    TABLE     �   CREATE TABLE public.lingue (
    id integer NOT NULL,
    codice_lingua character varying(5) NOT NULL,
    nome character varying(50) NOT NULL
);
    DROP TABLE public.lingue;
       public         heap    postgres    false            �            1259    17327    lingue_id_seq    SEQUENCE     �   CREATE SEQUENCE public.lingue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.lingue_id_seq;
       public          postgres    false    222            6           0    0    lingue_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.lingue_id_seq OWNED BY public.lingue.id;
          public          postgres    false    221            �            1259    17317    login    TABLE     �   CREATE TABLE public.login (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash text NOT NULL
);
    DROP TABLE public.login;
       public         heap    postgres    false            �            1259    17316    login_id_seq    SEQUENCE     �   CREATE SEQUENCE public.login_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.login_id_seq;
       public          postgres    false    220            7           0    0    login_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.login_id_seq OWNED BY public.login.id;
          public          postgres    false    219            �            1259    17336    opere_d_arte_id_seq    SEQUENCE     �   ALTER TABLE public.opere_d_arte ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.opere_d_arte_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    216            �           2604    17306    dettagli_opera id_dettaglio    DEFAULT     �   ALTER TABLE ONLY public.dettagli_opera ALTER COLUMN id_dettaglio SET DEFAULT nextval('public.dettagli_opera_id_dettaglio_seq'::regclass);
 J   ALTER TABLE public.dettagli_opera ALTER COLUMN id_dettaglio DROP DEFAULT;
       public          postgres    false    217    218    218            �           2604    17331 	   lingue id    DEFAULT     f   ALTER TABLE ONLY public.lingue ALTER COLUMN id SET DEFAULT nextval('public.lingue_id_seq'::regclass);
 8   ALTER TABLE public.lingue ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    222    222            �           2604    17320    login id    DEFAULT     d   ALTER TABLE ONLY public.login ALTER COLUMN id SET DEFAULT nextval('public.login_id_seq'::regclass);
 7   ALTER TABLE public.login ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    220    220            �           2604    17295    opere_d_arte immagine_id    DEFAULT     �   ALTER TABLE ONLY public.opere_d_arte ALTER COLUMN immagine_id SET DEFAULT nextval('public.artworks_immagine_id_seq'::regclass);
 G   ALTER TABLE public.opere_d_arte ALTER COLUMN immagine_id DROP DEFAULT;
       public          postgres    false    215    216    216            (          0    17303    dettagli_opera 
   TABLE DATA           r   COPY public.dettagli_opera (id_dettaglio, id, immagine_id, titolo, testo, coordinata_x, coordinata_y) FROM stdin;
    public          postgres    false    218   �,       ,          0    17328    lingue 
   TABLE DATA           9   COPY public.lingue (id, codice_lingua, nome) FROM stdin;
    public          postgres    false    222   R:       *          0    17317    login 
   TABLE DATA           <   COPY public.login (id, username, password_hash) FROM stdin;
    public          postgres    false    220   �:       &          0    17292    opere_d_arte 
   TABLE DATA           t   COPY public.opere_d_arte (id, immagine_id, titolo, autore, descrizione, percorso_immagine, sottotitolo) FROM stdin;
    public          postgres    false    216   �:       8           0    0    artworks_immagine_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.artworks_immagine_id_seq', 9, true);
          public          postgres    false    215            9           0    0    dettagli_opera_id_dettaglio_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.dettagli_opera_id_dettaglio_seq', 45, true);
          public          postgres    false    217            :           0    0    lingue_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.lingue_id_seq', 2, true);
          public          postgres    false    221            ;           0    0    login_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.login_id_seq', 1, true);
          public          postgres    false    219            <           0    0    opere_d_arte_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.opere_d_arte_id_seq', 15, true);
          public          postgres    false    223            �           2606    17299    opere_d_arte artworks_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.opere_d_arte
    ADD CONSTRAINT artworks_pkey PRIMARY KEY (id, immagine_id);
 D   ALTER TABLE ONLY public.opere_d_arte DROP CONSTRAINT artworks_pkey;
       public            postgres    false    216    216            �           2606    17310 "   dettagli_opera dettagli_opera_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.dettagli_opera
    ADD CONSTRAINT dettagli_opera_pkey PRIMARY KEY (id_dettaglio);
 L   ALTER TABLE ONLY public.dettagli_opera DROP CONSTRAINT dettagli_opera_pkey;
       public            postgres    false    218            �           2606    17335    lingue lingue_codice_lingua_key 
   CONSTRAINT     c   ALTER TABLE ONLY public.lingue
    ADD CONSTRAINT lingue_codice_lingua_key UNIQUE (codice_lingua);
 I   ALTER TABLE ONLY public.lingue DROP CONSTRAINT lingue_codice_lingua_key;
       public            postgres    false    222            �           2606    17333    lingue lingue_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.lingue
    ADD CONSTRAINT lingue_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.lingue DROP CONSTRAINT lingue_pkey;
       public            postgres    false    222            �           2606    17324    login login_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.login DROP CONSTRAINT login_pkey;
       public            postgres    false    220            �           2606    17326    login login_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.login DROP CONSTRAINT login_username_key;
       public            postgres    false    220            �           2620    17301 #   opere_d_arte before_insert_artworks    TRIGGER     �   CREATE TRIGGER before_insert_artworks BEFORE INSERT ON public.opere_d_arte FOR EACH ROW EXECUTE FUNCTION public.set_immagine_id();
 <   DROP TRIGGER before_insert_artworks ON public.opere_d_arte;
       public          postgres    false    224    216            �           2606    17311 1   dettagli_opera dettagli_opera_id_immagine_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dettagli_opera
    ADD CONSTRAINT dettagli_opera_id_immagine_id_fkey FOREIGN KEY (id, immagine_id) REFERENCES public.opere_d_arte(id, immagine_id);
 [   ALTER TABLE ONLY public.dettagli_opera DROP CONSTRAINT dettagli_opera_id_immagine_id_fkey;
       public          postgres    false    218    216    216    3465    218            (   �  x��YMo�F=[���l`V�hF_��#�ʰ�6�=쥇lr"��nr��E�������io9��쫪&��lGH,iD6��իWœ�'ON������~���4��l�����M�'����t~y���D=�͗/��?�E�n]X]�Z۪1^�L5K��վX���6]%f�n+wW��y��ASd��o����Uʟ����Q�7!q&LTh�����`����w:���Rצ���
��q���m|����T�KkoK�>�J�Ė�j�DU�q�������-
�+#�Y+�X�3�ki'*q�QkM��T�W�W�����X1P�+�6���'�GgӓS|��ON.Fi��x����=���`�s�k	����|�Qi������&�'�tj���(Ĳ.�ڤ06�-�(�wE�ܭ��(��u���n�M��.*m��r����Y�V�~=��MI�G�{�(֝Y�[f��H�Y,�j+�[W��LCa���͒�x��R�6�,��u��[��0��D��%e��x�uvpr�S>�OQ��9�����rT>��l��pk��l3�QN
�z��/�+�\VEj<�-X�����A�%�j�]��nK*F�Oi��r�Ԭh9EH�7�u�3�y���8x`�Մ.�w3�����$(
7�͸�/ՕY���؁E�^Tdq���銶�޺X;���vfg�����(CW��
�Pu0xD^ǃ$}��a�n���[�� ����K]�r>��}�E�,\�];)�k����c��)��+*� ��m�F4�I�>CJCLMɅ ���~��_ttC(k$��N�_Y�"�Q�K�W&��GtK2���Mh�,$;��I�R��d�Ա��H�
`A�gւC��T��b
G<��m��h�FR;4iP������l6J�;S�<��br�8U���F{��wzr0}O��榇r�$��z����o���������j�mh�I�#RK!�(�9�	��.\���=���������۬��e�̭���2g�e�
C]�	-Z""*�!�]�Λ!�n���67�O>vM�9�.9I�?@����G�c�P�'�.��7t�Œ/�ZS'=�����2��\��Q��7؏&&p`�f'��Nf�\�gӝb��� z��aW���S���A���->!�k�V9�t����-U��u��>LԾ��P֚;�G �RG&-�GH��4"��'��A}�7"�*�֣�2� t�P.��i�����%�ƈ�]` �Tp�5#���=�|��q�P���5x�����{��9���xq�xl��<��sK��9S��S=�n�:�1�Zm�t���W��K@���F���)��|���Ӄ�)�7�q���6��x�&N�&PM�TgC�}ŵ{euB��7�u�m��� {�%���6 ��H+:�����fϫЋ�Z7�Q��O�tcBmHq� �<X�-����h"*I՝�hk �Ol���P[�xԫs�3o���%{A�ɰs�2'���Ԣ��S�v�BU� �ciz�$s
ͽ,��B\����r��-K@b�$�9f�\�/�_�_g#�\r���w0P���ц�0��y�+.��u{��{g�������m�,���C!B������V�@:��$M^{y��Ҡ��ԟ��ߐ� 	��@���"��x݊Dg��c���ڍ 8�P��<q�B.���W��,��M� C�U;�"͌�t4D��XN	��8����Q��66�r�9Oq�R����
��7o1p�Εn�xB��5h��D�T(-�WI�!�IR�p �0��׆��tP�H6�)F����tU�B�����tB+z��֣ʆ	�G�ȓ��L�!����|hX�=	�����W��!��Y�R��<�џ@!��d��Ou�$v$6���~a{1�{��a��xv�t��>��Iև��u,w�$��)��׎fA������AgpPM�d���$ݮg:ހ���R�[���Cn�/1��[nR<��y^��\�B}ð�A�}lb��Hvл��E%�b-a���=�F�3l%`�B&t\I�� l��í�P&��h�x.~�#�ӳ-b~WTE�<=�1�bw�1����/����ht�]8l/c͎��L����L��m���G"�l��	Q�]�j�	��<_�j�`�א6G�>��R���P�t�*��Ċ8�w�H�ط�����t>;�������b��܌B�E���X��*s!���a:v�j�o�j����"s>#J����`~��rD�z&��H��'�T�'��y���m������)�2[��_��;�ӄ;��;�H{�dK[w�M�N�S:Z�����e�*�A[�"�0ʾ���u�kP������"8?6�Q-�_,-nB��T%�9I
�K���)��^�����9zׇ3?OL�į�Nn8��'��|�J�uv'w���	�w��$i	���ұ�����sP\q(Q\	�Jw��1|Ml�6�D=�$���V���i}����|3'E�v�jb�)d�1��ͥ��S��q�>�OG c|��r���r����	�`��1�]Fb����C��v�K�?�%�xivo�c;�7P}_�	�.�v���3�6<�jK49����{�hZw�*b��
����%{f�B�\F��G�wfX'��m���Ԭ��,!H.d.�=3�5��u��E���y|*��Ҿ�%Ʒ|��m\'�)�!����Fw��hQ����f�)��Q�-��//�%����n�颢u9cI��D�ȑ��t�� ^ֲ}Hh���\�P��`�̸\4GOs}D�\S�T]�4�p<�Xz�drZg���q{���ͺ]X#}�Me�~yr0�}�l��x?�N�y��UHߨ�tUY���Ԃ�2�m[�6soi�������/����Ƃ�a3S�����|��uGrJ$m?��F����}]<�������v��7������^��nEG��Kz�]^Z�IO�2���C��}��G�	6�����;���.V�y}��Z�Mz�S����4ݐV�:O9z��L��=�{�=ٛ�c��YXw[h����`�P� L����tۗ����Z�)��ۊ��t�)z�ܖ-&�%����>��;؎��9/M��fd4͙[��	S^zϧ;s���tT�ߖ 3��7nY�nnn�{L.w���',������$ct��^÷��9�]{�s�E�\o�༳+C��t~r�@5Hݒߎh�-���/�M��7,w�1�PG5��IO�фF���L�Z����D��.���=�	��>��"�F�:w2?xk�Kng[)��
u�#6lK���nC��r ����~�y��$�L\.Q�v'H} i��[)­�Q�����Љ�I���$�\����R��I��}�R���و�G�@�)'�r�� �3�Pk��n�y%2x�V*�o�Uh|�~~�Mގ��ף����t��      ,   (   x�3����,I��L���2�t��t�K��,������� ��o      *   R   x�3�LI��,�T1JR14R��)�)�p66�1��Տ��LN�O�3����ӏ��/M�3�/�H�H���H*-������ 3��      &   Y
  x��Xˎ�]�|1�v#Y���,؂ dA�"��f��h���գ���?��:��?��KV?���YxQ����"�=��sO��գ����橺y�7ު�U�h�	6)7��Y��ӣ���o�t�nV��ey�T���c�S��^��z�Cc]y��o���^��;���eSe$��^}r�cQ:��h�y�+�8��kg���[�Q�!�Fml��vP�_?���C��]���9)���p7��UI؝�퐹�k;h���U:��x;4�1Z�Z��w!�0�;�;5"���*����~�N9ڄ�Ǩ�|�-���M�V�i�q���3Y2�)Lq����s :���o���ՠc���,P�N	�JmDvv�+�	A�������k�E���V?��NYY�:�:*o5@�\R����2�0�p�S�V�Ӑ6��ՠN+u�9���s�X*�=R�7QXU�Q��ګ�L���XLE�����o? i�������ORo�m�mF���k�A ���˿�j}� @�'+�����yg�X���&�u�� 6�{%�D��0�M@�*���٢� ��Q05u���dg^K$= ���~@mH���`�TJ�Yԫ������b3�s󣣳d'����j3!������U�s�{YVc?�P=�gw6�ճ>T�Xl|�4��D�s7%�<(��y�ݫ� jo�/̄-K6������<$���[��H� b��@�mbU�G����9��h��WړX�ɫ�q�ps��%!��~.�F&�I��6D��>*y���vbA�	G�F �4��b ��B!H,��'d�_E�e2١֋����� ��Ԉ\��&� �赩!V�$]ۡ�]�Y-�T�Q_G�Ώb�c��3u��z{�NX��1hC���)j��w[��9��΄��޲��V��,#�&@�{"���2��J�]��NEA�d)���3`�ܩ�B'��{�}��$��V ���_Ry��.1St c�+��
���(zo�݇���J����y�/ �)�ǻJ�ƍ>����۲�`~���.����WTY��5�+�`C�/��� ;[������qZ�tXرu�	O�:�׉3q�Hb�E�I���gn�#'��G�tB�����k�@T�c0���.��7���u���DP�t�#Ե��q$�/xRg���'�$�-�ձ/#�������j;"Ly�CV��^
��2����ܪ'���-�E4Y�#5B�+��1<������Tj�]I��ew�}z�D��4�����Y���qrN �;OUŤ<���x��>�o����}ѼEt�;4#�Z9_�-���"��9�5�D�U11XP?���.��H1h-��aǺk�#�~8������/il�Ŋ�3La�^��t�=�SPX��@҄��b��`U؈����KK��kAw��x:��>��P6C�I�?'J��߳�;�����XW�V?NDZb��m6tV��k�4�rc������D��GH\	. O�ZZ��Y��р�� F�w@G���t�i��������k�h�F�Y��js ���V�&��o��������)8<���@s���0����5!���}j�	B�85l峁+,�J�@)�ӫ�@��ne�����Ys,�s^����g� ���X��4�'���X9 ��s��r��4�0����n81=�Z�f!q�c
�;("8���q�>vl@e�Ƀ왱��� �m�v2�9gZ��H���`���r�G��YOz�8� 6lDX�Su�#Do�a�h�Ji�.�B�@g�GӜM!��@�;���!~��`��l�Ҳ�����<٬@���m�vb
������!�LV�� �E3�u̠�9�Z�h��W,� E�	M'�kc`��`b�fZ��'
��*G�Y4_�+W`�@W��R�n_P6%���M�H�.�C�O���r����Ñ0�*�M{���F��$V;��GU2Q�d� �-<�O�}�d�NJ]Z�Ny��'*�{z��pW����ê�f�B���kxmX�� �g�K{�[2��:P�1 8GW������<��L	���5ڪsD��<�D�͗���8CT���S���J@[pf;B!��W<b���xY�z�H���6��$ú�V��pmW��o���=v���x1}���	k3�&FU3���E�y����2�~h�Xƒ�vG�=5[�]��B�PvD���%ܣ4��H���V&�a|�ݑ����u��������U����\E���t�{ �Ν�H�Ⱦ��6JOJza������2)�ᗼ�������m�D��J�U���~E�� xQ�6%���@pK���Z�-�8Q�9Dm����:��$,����9�p���ޢH,�����D��/96=���S~�W��o�`.�?���[���������4s9�\N3����4s9�\N3����4s9�\N3����4s9�\N3����4s9�\N3���?�i�L���������r���h.'�ˉ�r���h.'�ˉ�r���h.'�ˉ�r���h.'�ˉ�r���h.'�ˉ��D��<�۔�o^�^ݼ���+�?�m��w����^�㽷�"?]�>�.���]���b��b�N��}}}}�?��M     