from display import *
from matrix import *
from draw import *
from copy import deepcopy

ARG_COMMANDS = [ 'line', 'scale', 'move', 'rotate', 'save', 'circle', 'bezier', 'hermite', 'box', 'sphere', 'torus' ]

def parse_file( fname, edges, polygons, transform, screen, color ):

    f = open(fname)
    lines = f.readlines()

    stack = []
    new_m = new_matrix()
    ident(new_m)
    print_matrix(new_m)
    stack.append(new_m)
    
    step = 0.1
    c = 0

    while c < len(lines):
        line = lines[c].strip()
        #print ':' + line + ':'

        if line in ARG_COMMANDS:            
            c+= 1
            args = lines[c].strip().split(' ')
            #print 'args\t' + str(args)

        if line == 'sphere':
            #print 'SPHERE\t' + str(args)
            add_sphere(polygons,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult( stack[-1], polygons )
            draw_polygons(polygons, screen, color)
            polygons[:] = []
            
        elif line == 'torus':
            #print 'TORUS\t' + str(args)
            add_torus(edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step)
            matrix_mult( stack[-1], polygons)
            draw_polygons(polygons, screen, color)
            polygons[:] = []

        elif line == 'box':
            add_box(edges,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( stack[-1], polygons)
            draw_polygons(polygons, screen, color)
            polygons[:] = []

        elif line == 'circle':
            #print 'CIRCLE\t' + str(args)
            add_circle(edges,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), 0.005)
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges[:] = []

        elif line == 'hermite' or line == 'bezier':
            #print 'curve\t' + line + ": " + str(args)
            add_curve(edges,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      step, line)   
            matrix_mult( cstack[-1], edges )
            draw_polygons(edges, screen, color)
            edges[:] = []

        elif line == 'line':            
            #print 'LINE\t' + str(args)

            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult( cstack[-1], edges )
            edges[:] = []

        elif line == 'scale':
            #print 'SCALE\t' + str(args)
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[-1], t)
            stack[-1] = t

        elif line == 'move':
            #print 'MOVE\t' + str(args)
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[-1], t)
            stack[-1] = t

        elif line == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(args[1]) * (math.pi / 180)
            
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(stack[-1], t)
            stack[-1] = t
         
        elif line == 'pop':
            if len(stack) > 1:
                stack.pop()
            else:
                print 'cannot pop ident stack'

        elif line == 'push':
            stack.append(deepcopy(stack[-1]))

                
        elif line == 'clear':
            edges = []
            
        elif line == 'ident':
            ident(stack)

        elif line == 'apply':
            matrix_mult( stack[-1], edges )

        elif line == 'display' or line == 'save':
            #clear_screen(screen)
            #draw_lines(edges, screen, color)
            #draw_polygons(edges, screen, color)

            if line == 'display':
                print edges
                display(screen)
            else:
                save_extension(screen, args[0])
            
        c+= 1
