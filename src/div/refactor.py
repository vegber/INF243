def EEA(a, s_x, p): #Extended Euclidean Algoritm
        old_r = a;
        r = s_x;
        buffer_r = old_r;
        old_s = 1;
        s = 0;
        buffer_s = old_s;
        old_t = 0;
        t = 1;
        buffer_t = old_t;
        while old_r.degree() >= p:
            q = old_r // r;
            old_r = r;
            r = buffer_r - (q*r);
            old_s = s;
            s = buffer_s - (q*s);
            old_t = t;
            t = buffer_t - (q*t);
            buffer_r = old_r;
            buffer_s = old_s;
            buffer_t = old_t;
        return old_r, old_s, old_t