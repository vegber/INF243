import numpy as np


def get_connected_bits(H, i):
    """
    Computes list of elements of N(i)-j:
    List of variables (bits) connected to Parity node i.

    """
    m, n = H.shape
    return [a for a in range(n) if H[i, a]]


def get_connected_nodes(tH, j):
    """
    Computes list of elements of M(j):
    List of nodes (PC equations) connecting variable j.

    """
    return get_connected_bits(tH, j)


def get_Nm_M_n(H):
    m, n = H.shape
    tH = np.transpose(H)

    Bits = [get_connected_bits(H, i) for i in range(m)]
    Nodes = [get_connected_nodes(tH, j) for j in range(n)]

    return Bits, Nodes


import numpy as np


def ldpc_decode_belief_propagation(symbol, H, max_iter=2):
    """
    A LDPC decoder based on the belief propagation method.

    Parameters:
        symbol: received symbols
        H: check matrix
        max_iter: maximum number of iterations (default: 2)

    Returns:
        decoded message bits
    """
    # Extract matrix dimensions
    num_check_bits, num_coding_bits = H.shape
    num_message_bits = num_coding_bits - num_check_bits

    # Initialize variables
    beta = np.zeros((num_check_bits, num_coding_bits))
    alpha = np.zeros((num_check_bits, num_coding_bits))
    decide = np.zeros(num_coding_bits)

    # Find the nonzero elements
    N_m, H_m = get_Nm_M_n(H)
    # Initialize beta matrix
    for check_id in range(num_check_bits):
        connected_bits = N_m[check_id]
        beta[check_id, connected_bits] = symbol[connected_bits]

    # Message update
    for iteration in range(max_iter):
        # Step 2: Horizontal message passing
        for bit_id in range(num_coding_bits):
            connected_checks = H_m[bit_id]
            for check_id in connected_checks:
                connected_bits = N_m[check_id]
                # Calculate the product of the tanh functions for the connected bits
                X = np.prod(np.tanh(0.5 * beta[check_id, connected_bits]))
                # Compute the alpha values (check node to bit node messages)
                alpha[check_id, bit_id] = 2 * np.arctanh(X)

            # Step 2: Vertical message passing
            Mij = [check_id for check_id in connected_checks if check_id != bit_id]
            # Compute the beta values (bit node to check node messages)
            beta[:, bit_id] = symbol[bit_id] + np.sum(alpha[Mij, bit_id])

        # Step 3: Compute the updated messages and decisions
        for bit_id in range(num_coding_bits):
            connected_checks = H_m[bit_id]
            # Compute the updated message for the bit node
            m_bit = np.sum(alpha[connected_checks, bit_id]) + np.sum(beta[connected_checks, bit_id])
            # Compute the decision for the bit node
            decide[bit_id] = symbol[bit_id] + m_bit

    # Soft decision: Decode the message bits based on the decisions
    decoded_message_bits = np.zeros(num_message_bits)
    for i in range(num_message_bits):
        if decide[i + num_check_bits] < 0:
            decoded_message_bits[i] = 1

    return decoded_message_bits

