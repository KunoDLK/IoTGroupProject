$fs = 1; 
$fa = 30; 

PCB_Width = 46.0;
PCB_Depth = 1.5;
PCB_Height = 21.0;
PCB_Sonic_Height = 11;
PCB_Sonic_Radius = 8;
PCB_Sonic_Offset = 13.0;
PCB_Hole_Radius = 0.7;
PCB_Hole_X_Offset = 21.25;
PCB_Hole_Y_Offset = 8.75;

Sonic_Support_Depth = 1.5;

PI_Height = 85;
PI_Width = 56;
PI_Support_Height = 10;
PI_Support_Width = 5;
PI_Support_Offset_Y = 24.5;
PI_Support_X_Offset_1 = 19;
PI_Support_X_Offset_2 = 39;

Joint_dove_height = 8;
Joint_dove_depth = 5;
Joint_dove_rear_width = 16;
Joint_dove_front_width = 8;

showPI = false;
splitView = false;


if (splitView)
{
    intersection()
    {
        Viewer();
        
        translate([-PI_Height/2,0,0]) cube([PI_Height, PI_Width, PCB_Sonic_Height + PCB_Depth + PI_Support_Height + 3]);
    }
}
else
{
    Viewer();
}

module Viewer()
{
    if (showPI)
    {
        translate([0,0,PI_Support_Height + PCB_Depth + PCB_Sonic_Height]) RPi();
    }

    Main();
}


module Main()
{
    union()
    {
        difference()
        {
            color("Yellow") Base();
        
            rotate([180,0,0]) 
            {
                translate([0,0,-PCB_Depth - PCB_Sonic_Height]) 
                {
                    color("Red") Utrasonic();
                    color("blue")
                    {
                        cutoutLengthWidth = PCB_Height - (4 * ((PCB_Height / 2) - (PCB_Hole_Y_Offset)));
                        cutoutWidthLength = PCB_Width - (4 * ((PCB_Width / 2) - (PCB_Hole_X_Offset)));
                        
                        linear_extrude(PCB_Depth + PCB_Sonic_Height - Sonic_Support_Depth) union()
                        {
                            square([PCB_Width,cutoutLengthWidth], center = true);
                            square([cutoutWidthLength, PCB_Height], center = true);
                        }
                    }
                }
                
            }
        }
        
        translate([PI_Support_X_Offset_1,PI_Support_Offset_Y,PCB_Depth + PCB_Sonic_Height]) Support();
        translate([-PI_Support_X_Offset_2,PI_Support_Offset_Y,PCB_Depth + PCB_Sonic_Height]) Support();
        translate([PI_Support_X_Offset_1,-PI_Support_Offset_Y,PCB_Depth + PCB_Sonic_Height]) Support();
        translate([-PI_Support_X_Offset_2,-PI_Support_Offset_Y,PCB_Depth + PCB_Sonic_Height]) Support();
    }
}

module Base()
{
    render()
    {
        difference()
        {
            linear_extrude(PCB_Depth + PCB_Sonic_Height)
            {
                square([PI_Height,PI_Width], center = true);
            }
            
            linear_extrude(Joint_dove_height)
            {
                union()
                {
                    rotate([0,0,0]) translate([0, -PI_Width / 2,0]) Dovetail2d();
                    rotate([0,0,90]) translate([0, -PI_Height / 2,0]) Dovetail2d();
                    rotate([0,0,180]) translate([0, -PI_Width / 2,0]) Dovetail2d();
                    rotate([0,0,270]) translate([0, -PI_Height / 2,0]) Dovetail2d();
                }
            }
        }
    }
}

module Dovetail2d()
{
    frontOffset = Joint_dove_front_width / 2;
    rearOffset = Joint_dove_rear_width / 2;
                
    polygon([[-frontOffset,0],
    [frontOffset,0],
    [rearOffset, Joint_dove_depth],
    [-rearOffset, Joint_dove_depth]]);
}

module RPi()
{
    difference()
    {
        
        linear_extrude(1.4)
            square([PI_Height, PI_Width], center = true); 
    
        translate([-(PI_Height / 2) + 3.5,-(PI_Width / 2) + 3.5,0])
        {
            Hole();
            translate([58, 0 ,0])
            {
                Hole();
            }
        }
        translate([-(PI_Height / 2) + 3.5,+(PI_Width / 2) - 3.5,0])
        {
            Hole();
            translate([58, 0 ,0])
            {
                Hole();
            }
        }
    }
}

module Hole()
{
    cylinder(h = 3, r = 2.7 / 2);
}
   
module Support()
{
    cylinder(h =PI_Support_Height, r = PI_Support_Width / 2);
    translate([0,0,PI_Support_Height])
    {
        Hole();
    }
}

module Utrasonic() {
    
    difference()
    {
        
        union() {
            translate([-(PCB_Width / 2), -(PCB_Height / 2), 0])
            {
                cube([PCB_Width, PCB_Height, PCB_Depth]);
            }
            translate([PCB_Sonic_Offset, 0, PCB_Depth])
            {
                cylinder(h = PCB_Sonic_Height, r = PCB_Sonic_Radius);
            }
            translate([-PCB_Sonic_Offset, 0, PCB_Depth])
            {
                cylinder(h = PCB_Sonic_Height, r = PCB_Sonic_Radius);
            }
        }
        translate([PCB_Hole_X_Offset, PCB_Hole_Y_Offset, -1])
        {
            cylinder(h = PCB_Depth + 2, r = PCB_Hole_Radius);
        }
        translate([-PCB_Hole_X_Offset, PCB_Hole_Y_Offset, -1])
        {
            cylinder(h = PCB_Depth + 2, r = PCB_Hole_Radius);
        }
        translate([PCB_Hole_X_Offset, -PCB_Hole_Y_Offset, -1])
        {
            cylinder(h = PCB_Depth + 2, r = PCB_Hole_Radius);
        }
        translate([-PCB_Hole_X_Offset, -PCB_Hole_Y_Offset, -1])
        {
            cylinder(h = PCB_Depth + 2, r = PCB_Hole_Radius);
        }
    }
}