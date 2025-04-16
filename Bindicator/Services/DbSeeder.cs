// Services/DbSeeder.cs
using Bindicator.Data;
using Bindicator.Models;

public class DbSeeder
{
    public static async Task SeedAsync(ApplicationDbContext context)
    {
        if (!context.SensorReadings.Any())
        {
            var now = DateTime.UtcNow;

            var bins = new List<SensorData>
            {
                // Bin 1 (spike from 40 → 85)
                new() { Postcode = "TS16", Street = "Formby Walk", BinNumber = 1, FillLevel = 40, Weight = 8.2f, Density = 1.1f, Timestamp = now.AddMinutes(-30), Latitude = 54.5631, Longitude = -1.3123 },
                new() { Postcode = "TS16", Street = "Formby Walk", BinNumber = 1, FillLevel = 85, Weight = 16.2f, Density = 1.5f, Timestamp = now.AddMinutes(-15), Latitude = 54.5631, Longitude = -1.3123 },

                // Bin 2 (normal → spike 30 → 65)
                new() { Postcode = "TS16", Street = "Alder Crescent", BinNumber = 2, FillLevel = 30, Weight = 6.8f, Density = 0.9f, Timestamp = now.AddMinutes(-20), Latitude = 54.5645, Longitude = -1.3105 },
                new() { Postcode = "TS16", Street = "Alder Crescent", BinNumber = 2, FillLevel = 65, Weight = 12.4f, Density = 1.1f, Timestamp = now.AddMinutes(-5), Latitude = 54.5645, Longitude = -1.3105 },

                // Bin 3 (no spike, slow climb — should show no spike)
                new() { Postcode = "TS17", Street = "Oakwood Drive", BinNumber = 3, FillLevel = 15, Weight = 4.2f, Density = 0.6f, Timestamp = now.AddMinutes(-25), Latitude = 54.5662, Longitude = -1.3150 },
                new() { Postcode = "TS17", Street = "Oakwood Drive", BinNumber = 3, FillLevel = 25, Weight = 6.4f, Density = 0.8f, Timestamp = now.AddMinutes(-10), Latitude = 54.5662, Longitude = -1.3150 }
            };

            context.SensorReadings.AddRange(bins);
            await context.SaveChangesAsync();
        }
    }
}