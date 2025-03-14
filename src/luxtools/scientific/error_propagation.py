from typing import Set

import torch


def get_leaf_nodes(tensor) -> Set[torch.Tensor]:
    """Traverses the computation graph of a tensor and returns the leaf nodes that require gradients.

    Args:
        tensor (torch.Tensor): tensor whose graph we should traverse

    Returns:
        Set[torch.Tensor]: leaf nodes that require gradients
    """
    leaves = set()
    visited = set()

    def traverse(node):
        if node in visited:
            return
        visited.add(node)

        if hasattr(node, 'variable'):
            var = node.variable
            if var.is_leaf and var.requires_grad:
                leaves.add(var)
        else:
            if hasattr(node, 'next_functions'):
                for next_node, _ in node.next_functions:
                    if next_node is not None:
                        traverse(next_node)

    if tensor.grad_fn is not None:
        traverse(tensor.grad_fn)

    return leaves


def Variable(tensor: torch.Tensor, sigma: torch.Tensor) -> torch.Tensor:
    """Attaches the uncertainty to a tensor.

    Args:
        tensor (torch.Tensor): The tensor to which the uncertainty is to be attached.
        sigma (torch.Tensor): The uncertainty to be attached to the tensor.
    """
    # TODO: create a real object instead of monkey patching and integrate with printing
    tensor.sigma = sigma
    return tensor

def get_error(f: torch.Tensor, zero_grad=True) -> torch.Tensor:
    """Computes the uncertainty of f.

    Example:
    =============

    ```
    x = torch.tensor([1.0, 3.0], dtype=torch.float32, requires_grad=True)
    x.sigma = torch.tensor([0.1,0.2], dtype=torch.float32)
    y = torch.tensor([2.0, 4.0], dtype=torch.float32, requires_grad=True)
    y.sigma = torch.tensor([0.2,0.3], dtype=torch.float32)

    f = x*y

    error = get_error(f)
    >>> tensor([0.2828, 1.2042])
    ```
    Explaination:
    =============
    If f is a function of some leaf nodes (x,y,z,...)
    each of which having a uncertainty x.sigma, y.sima, z.sigma, ...

    Then the uncertainty of f is given by:

    $$\sigma_f = \sqrt{(\frac{\partial f}{\partial x} \sigma_x)^2 + (\frac{\partial f}{\partial y} \sigma_y)^2 + (\frac{\partial f}{\partial z} \sigma_z)^2 + ...}$$

    This function traverses the computational graph of f and computes the uncertainty of f.

    Args:
        f (torch.Tensor): The tensor for which the uncertainty is to be computed.
        zero_grad (bool): Whether to zero the gradients after computing the uncertainty.
                          Should probably be set to True, unless you need to inspect the gradients afterwards.

    Returns:
        torch.Tensor: The uncertainty of f.
    """
    # Compute gradients
    f.backward(torch.ones_like(f), retain_graph=True)

    # Get leaf nodes
    leaf_nodes = get_leaf_nodes(f)

    # calculate error
    error = torch.zeros_like(f)
    for leaf in leaf_nodes:
        error += (leaf.grad*leaf.sigma)**2

    error = torch.sqrt(error)

    # zero out leaf_nodes
    if zero_grad:
        for leaf in leaf_nodes:
            leaf.grad.zero_()

    return error