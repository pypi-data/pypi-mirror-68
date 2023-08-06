
import itertools
import svgwrite
import io

class SVGRenderer:
    """Renders feyn objects to matplotlib axes."""


    def layout_2d(graph):
        locs = [None]*len(graph)
        for layer, interactions in itertools.groupby(graph, lambda g: g.depth):
            interactions = list(interactions)
            sz = len(interactions)
            center = (sz-1) / 2
            for ix, interaction in enumerate(interactions):
                locs[interaction._location] = (layer+1, ix-center)

        return locs



    @staticmethod
    def rendergraph(graph, label=None):
        locs = SVGRenderer.layout_2d(graph)

        # Move y values so the smallest is 0
        min_y = min([loc[1] for loc in locs])
        locs = [(1+loc[0]*120, (loc[1]-min_y)*60+5) for loc in locs]
        
        
        max_x = max([loc[0] for loc in locs])
        max_y = max([loc[1] for loc in locs])

        nodew = 80
        nodeh = 30
        
        w = max_y+nodeh+40
        h = max(max_x+nodew+2, 450)
        drawing = svgwrite.Drawing(
            profile="tiny", 
            size=(h, w)
        )

        for ix, interaction in enumerate(graph):
            loc = locs[ix]
            if interaction.type in ("cat", "cont", "fixed"):
                color = "#00F082"
                stroke = "#808080"
            else:
                color = "#FAFAFA"
                stroke = "#ff1ec8"

            # The node rect
            rect = drawing.rect(
                (loc[0], loc[1]), 
                (80,30), 
                fill=color, 
                stroke=stroke, 
                stroke_width=1
            )
            tooltip = svgwrite.base.Title(interaction._tooltip)
            rect.add(tooltip)
            drawing.add(rect)

            # The node text
            l = interaction.name
            if len(l) > 10:
                l = l[:10]+".."
            txt = drawing.text(l, 
                            insert=(loc[0]+nodew/2, loc[1]+nodeh/2+4), 
                            fill='#202020', 
                            text_anchor="middle", 
                            font_size=11, 
                            font_family="monospace")
            drawing.add(txt)
            
            for ord, src_ix in enumerate(interaction.sources):
                src_loc = locs[src_ix]
                x0 = src_loc[0]+nodew
                y0 = src_loc[1]+nodeh/2
                    
                x1 = loc[0]
                y1 = loc[1]+nodeh/2
                if len(interaction.sources)==2:
                    y1 += 9-(ord*18)
                    
                # Connecting lines
                line = drawing.line(
                    (x0,y0),(x1, y1), 
                    stroke="#c0c0c0"
                )
                drawing.add(line)

                # The ordinal markers
                txt = drawing.text(f"x{ord}", 
                                insert=(x1+5, y1+3), 
                                fill='#202020', 
                                text_anchor="middle", 
                                font_size=7, 
                                font_family="monospace")
                drawing.add(txt)


        if label:
            txt = drawing.text(label, 
                insert=(0, max_y+nodeh+28), 
                fill='#202020', 
                font_size=12, 
                font_family="monospace")
            drawing.add(txt)
        
        if graph.loss_epoch is not None:
            loss_label = "Loss: %.2E" % (graph.loss_epoch)
            loc = locs[-1]
            txt = drawing.text(loss_label, 
                            insert=(loc[0]+nodew/2, loc[1]+1.4*nodeh), 
                            fill='#202020', 
                            text_anchor="middle", 
                            font_size=11, 
                            font_family="monospace")
            drawing.add(txt)

        f = io.StringIO()
        drawing.write(f)
        return f.getvalue()


    @staticmethod
    def renderqgraph(graph):
        """
        Render an entire QGraph.
        """
        raise Exception("Not implemented")

