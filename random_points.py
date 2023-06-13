from manim import *
import numpy as np
import math
import random as ran


class MonteCarlo(Scene):

    def construct(self):

        offset = (-4, 0, 0)

        circle = Circle(radius=2, color=RED)
        circle.move_to(offset)

        square = Rectangle(width=4, height=4)
        square.move_to(offset)

        self.add(circle)
        self.add(square)
        self.wait(1)
        font_size = 24
        point_text, point_number = point_label = VGroup(
            Text("Todos os pontos : ", font_size=font_size),
            DecimalNumber(
                0,
                show_ellipsis=False,
                num_decimal_places=0,
                font_size=font_size
            )
        )

        in_text, in_number = in_label = VGroup(
            Text("Pontos no círculo : ", font_size=font_size),
            DecimalNumber(
                0,
                show_ellipsis=False,
                num_decimal_places=0,
                font_size=font_size
            )
        )

        pi_text, pi_number = pi_label = VGroup(
            MathTex(r"\pi: ", font_size=font_size*2),
            DecimalNumber(
                0,
                show_ellipsis=True,
                num_decimal_places=4,
                font_size=font_size*2
            )
        )
        point_label.arrange(RIGHT)
        in_label.arrange(RIGHT)
        pi_label.arrange(RIGHT)

        in_label.next_to(circle, direction=DOWN)
        point_label.next_to(in_label, direction=DOWN)
        pi_label.next_to(circle, direction=UP)

        self.add(point_label, in_label, pi_label)

        count_all = 0
        c = 0
        apx_pi = 0

        point_number.add_updater(lambda m: m.set_value(count_all+1))
        in_number.add_updater(lambda m: m.set_value(c+1))
        pi_number.add_updater(lambda m: m.set_value(apx_pi))

        ran.seed(1)
        step = 10
        number_of_interations = 10**4
        list_values = [10**i for i in range(0,int(np.log(number_of_interations*step)/ np.log(step))+1)]
        #import ipdb;ipdb.set_trace()
        print(list_values)
        #, 
        axes = Axes(x_range=[0, 5, 1],y_range=[2, 3.5, 1], y_length=4,x_length=5,
                    tips=False,x_axis_config={"scaling": LogBase(custom_labels=True)}, axis_config={'include_ticks': False}).move_to((3, 0, 0))
        labels = axes.get_axis_labels(
            x_label="Iteracoes", y_label=r'\pi')
        pi_graph = Line(
            start=axes.coords_to_point(1, np.pi),
            end=axes.coords_to_point(10**5, np.pi)
        )
        self.play(Create(VGroup(axes, labels, pi_graph)))
        dots = []
        pi_values = []
        pi_coordenates = []
        for i in range((step*number_of_interations)+1):
            pos = (-6 + ran.random() * 4, -2 + ran.random() * 4, 0)
            if ((pos[0] + 4) ** 2 + pos[1] ** 2 < 4):
                d = Dot(color=RED, radius=0.04)
                c += 1
            else:
                d = Dot(color=GREEN, radius=0.04)
            d.move_to(pos)

            dots.append(d)

            if i in list_values and i>=100:
                #print(i)
                animate_dots = VGroup(
                    *dots[int(i/step):i]
                )
                scale_x = [(x)/(step) for x in range(int(i/step), i)]
                #
                
                log_scale_x = (np.log(scale_x)/np.log(10))*10+1
                #import ipdb;ipdb.set_trace()
                round_pi = [round(num, 4) for num in pi_values[int(i/step):i]]
                line = axes.plot_line_graph(
                    x_values=scale_x, y_values=round_pi, add_vertex_dots=False)
                # self.play(Create(line, run_time=0.1))
                #ipdb.set_trace()
                self.play(Create(VGroup(line, animate_dots), run_time=.25 + .1*list_values.index(i)), subcaption_duration=5)
            count_all = i
            apx_pi = c/(i+1) * 4
            pi_values.append(apx_pi)
            print(i, apx_pi)
        self.wait(2)