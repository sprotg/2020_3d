from ur_programmer import UR_programmer

prog = UR_programmer("10.130.58.11", simulate=False)

prog.move_path([[-0.404,-0.416],[-0.304,-0.416],[-0.304,-0.316],[-0.404,-0.316]])
