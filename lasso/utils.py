
def run_from_ipython():
    """
    Is the system running from within IPython?
    """
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

def ipython_except_hook(shell,etype,evalue,tb,tb_offset=None):
    shell.showtraceback((etype,evalue,tb),tb_offset=tb_offset)
    if etype.__name__=='ServiceException':
        from IPython.core.display import HTML,display
        display(HTML(str(evalue)))