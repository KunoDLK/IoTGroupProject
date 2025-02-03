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



inner_height = total_height - top_platform_thickness - bottom_platform_thickness;
pie_angle = (360 / number_of_legs);

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
    // On top of the Platform
    translate([0,0, PCB_Depth + PCB_Sonic_Height - top_platform_thickness]) rotate([0,180,0])
    {
        color("Red") Utrasonic();
    }
    
    difference() {
        #cube([20,20,PCB_Sonic_Height + PCB_Depth - top_platform_thickness]);
        
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