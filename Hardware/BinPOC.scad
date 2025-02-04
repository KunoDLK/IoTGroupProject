$fs = 0.2; 
$fa = 5; 

wall_thickness = 5.0;
top_platform_thickness = 4.0;
bottom_platform_thickness = 8.0;
total_height = 250.0;
outer_radius = 100.0;
number_of_legs = 3;
leg_radial_thickness = 20.0;

PCB_Width = 45.0;
PCB_Depth = 1.5;
PCB_Height = 20.0;
PCB_Sonic_Height = 12.0;
PCB_Sonic_Radius = 8.0;
PCB_Sonic_Offset = 13.0;
PCB_Hole_Radius = 1.0;
PCB_Hole_X_Offset = 20.5;
PCB_Hole_Y_Offset = 8.25;
PCB_Hole_Clearence = 1;

Sonic_Support_X = 40;
Sonic_Support_Y = 40;
Sonic_Vertical_Clearence = 5;

PI_Height = 85;
PI_Width = 56;
PI_Support_Height = 10;
PI_Support_Width = 5;

inner_height = total_height - top_platform_thickness - bottom_platform_thickness;
pie_angle = (360 / number_of_legs);

Main();

translate([outer_radius * 3, 0 ,-(total_height - top_platform_thickness)])
{
    intersection()
    {
        Main();
        translate([0,0,total_height - top_platform_thickness])
        {
            cylinder(h = 50, r = outer_radius);
        }    
    }
}

module Main()
{
    //Subtract smaller cylinder to create hollow
    difference() {
        cylinder(h = total_height, r = outer_radius);
        
        translate([0, 0, bottom_platform_thickness])
        { 
            cylinder(h = inner_height, r = outer_radius - wall_thickness);
        }
        
        // Subtract three Pies to leave the legs
        translate([0, 0, bottom_platform_thickness])
        {
            for (i = [1:number_of_legs]) 
            {
                rotate([0, 0, i * pie_angle]) 
                    rotate_extrude(angle=pie_angle - leg_radial_thickness)
                        square(inner_height,  outer_radius - wall_thickness);    
            }
        }       
        translate([0,0,total_height - top_platform_thickness + PCB_Sonic_Height])
        {
            rotate([0,180,0])
            {
                Utrasonic();
            }
        }
    }
    translate([0,0,total_height])
    {    
        //Ontop of the suport frame
        sonic_height = PCB_Sonic_Height + PCB_Depth - top_platform_thickness;
        
        // Ultrasonic sensor holder
        difference() 
        {
            translate([-(Sonic_Support_X / 2), -(Sonic_Support_Y / 2), 0])
            {
                cube([Sonic_Support_X,Sonic_Support_Y,sonic_height]);
            }
            
            sonic_subtract_X = PCB_Hole_X_Offset - PCB_Hole_Radius - PCB_Hole_Clearence;
            sonic_subtract_Y = PCB_Hole_Y_Offset - PCB_Hole_Radius - PCB_Hole_Clearence;
    
            translate([-(PCB_Width / 2), -(sonic_subtract_Y), 0])
            {
                cube([PCB_Width, sonic_subtract_Y * 2, sonic_height + Sonic_Vertical_Clearence]);
            }
            
            translate([-(sonic_subtract_X), -(PCB_Height / 2), 0])
            {
                cube([sonic_subtract_X * 2, PCB_Height, sonic_height + Sonic_Vertical_Clearence]);
            }
            translate([0,0, PCB_Depth + PCB_Sonic_Height - top_platform_thickness]) rotate([0,180,0])
            {
                color("Red") Utrasonic();
            }
        }
        // Rasbery PI Suport
        translate([0,0,sonic_height])
        {
            translate([-(PI_Height / 2) + 3.5,-(PI_Width / 2) + 3.5,0])
            {
                Support();
                translate([58, 0 ,0])
                {
                    Support();
                }
            }
            translate([-(PI_Height / 2) + 3.5,+(PI_Width / 2) - 3.5,0])
            {
                Support();
                translate([58, 0 ,0])
                {
                    Support();
                }
            }
        }
    }
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
    cylinder(h = 1.4, r = 2.7 / 2);
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