$fn = $preview ? 50 : 500;

/* [Base Settings] */
Base_Radius = 60;
Base_Thickness = 2;
Base_Wall_Thickness = 8;
Base_Height = 15;

/* [FSR Settings] */
FSR_Radius = 9.5;
FSR_Ribbon_Width = 8;
FSR_Ribbon_Length = 48; 
FSR_Ribbon_Thickness = 0.5; 

/* [Port Settings] */
Port_Width = 30;
Port_Floor_Depth = 0.5;
Port_Depth = 20;

Base();

module Base()
{
        difference() {

                linear_extrude(Base_Height)
                circle(Base_Radius);

                translate([0, 0, Base_Thickness]) {
                        linear_extrude(Base_Height - Base_Thickness + 0.1)
                        circle(Base_Radius - Base_Wall_Thickness);
                } 

                color("blue") translate([0, 0, Base_Thickness - FSR_Ribbon_Thickness]) {
                        linear_extrude(FSR_Ribbon_Thickness + 0.1)
                        {
                                circle(FSR_Radius);
                                translate([-FSR_Ribbon_Width / 2,0,0])
                                        square(size=[FSR_Ribbon_Width, FSR_Ribbon_Length]);
                        }
                }

                portHeight = Base_Thickness - FSR_Ribbon_Thickness - Port_Floor_Depth;

                color("red")
                translate([-Port_Width / 2,Base_Radius - Port_Depth,portHeight])
                linear_extrude(Base_Height - portHeight + 0.1)
                {
                        square(size=[Port_Width, Port_Depth]);        
                }
        }
}