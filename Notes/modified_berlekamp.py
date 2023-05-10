# assume f(x) = x^2 +1 = [1, 0, 1]
f_x = x^5 + x^4+ x^3 + x^2 + x + 1
def Berlekamp_decoding(f_x):  
    """
    input: f(x): sum_{i=0}^{n} a_i*x^i = a_0 + a_1*x + ... + a_n-1 x^n-1
    return: sigma^
    """
    # f_x = vector(F, f_x)
    f = (f_x).dict()
    # assumen the first nonzero coefficient of f is one  
    sigma, tau, omega, gamma, = dict(), dict(), dict(), dict()
    
    D, B = dict(), dict()
    # quick fix 
    D[-1], B[-1] = 0, 0
    
    if f[0] == 1: 
        sigma[0], tau[0], omega[0], gamma[0] = 1, 1, 1, 0
        D[0], B[0] = 0, 0, 
     
    else: 
        sigma[0], tau[0], omega[0], gamma[0] = 1, 1, 0, -1
        D[0], B[0] = 0, 1
    
    k = 0 
    while k <= n - 2: 
        # take delta k as the coefficient of x^k in f*sigma_k
        fdelta_k = (f_x * sigma[k])
        delta_k = fdelta_k.list()[k+1]
        # now find coefficient of x^k from tmp 
        sigma[k+1] = sigma[k] - delta_k * x * tau[k]
        omega[k+1] = omega[k] - delta_k * x * gamma[k]
        
        if delta_k == 0 or (D[k] > ((k + 1) / 2)) or (D[k] == ((k + 1) / 2) and B[k] == 0): 
            D[k + 1] = D[k]
            B[k + 1] = B[k]
            tau[k+1] = x * tau[k]
            gamma[k+1] = x * gamma[k]
        
       # From org. paper, this is redundant 
       #  elif delta_k != 0 and (((B[k-1] == 0) and D[k-1] <= (k - floor(n/2) - 1)) or (B[k-1])==1 and D[k-1] <= k - floor((n-1)/2) - 1):
       #      sigma_hat = x ^(n-k) * sigma[k]
       #      omega_hat = x ^(n-k) * omega[k]
       #      N_hat = n - k + D[k - 1] + 1 - B[k - 1]
       #      # assert (f_x*sigma_hat) == (omega_hat % x^n)
       #     return sigma_hat, omega_hat, N_hat
        else:  
            D[k+1] = (k+1) - D[k]
            B[k+1] = 1 - B[k]
            tau[k+1] = sigma[k] / delta_k
            gamma[k+1] = omega[k] / delta_k 
        k = k + 1 
    sigma_hat = sigma[n-1]
    omega_hat = omega[n-1]
    N_hat     = D[n-1] + 1 - B[n-1]
    
    # assert int(sigma_hat.degree()) <= int(floor(n/2)), f"sigma was: {sigma_hat.degree()}"
    # assert int(omega_hat.degree()) <= int(floor((n-1)/2))
    # print(f"f_x * omega_hat congruent with omega % g: {(f_x * omega_hat) == omega_hat % g }")
    return sigma_hat, omega_hat, N_hat