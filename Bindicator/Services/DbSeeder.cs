using Bindicator.Data;
using Bindicator.Models;
using Microsoft.EntityFrameworkCore;

public class DbSeeder
{
    /// <summary>
    /// Seeds the database with initial sensor data if the table is empty.
    /// </summary>
    /// <param name="context">The database context to use for seeding data.</param>
    /// <returns>A task that represents the asynchronous operation.</returns>
    public static async Task SeedAsync(ApplicationDbContext context)
    {
        // ✅ Ensure DB exists
        await context.Database.EnsureCreatedAsync();

        // ✅ Exit if data already exists
        if (await context.SensorReadings.AnyAsync())
            return;

        var now = DateTime.UtcNow;

        var bins = new List<SensorData>
        {
            // Bin 1 – Gradual, then spike
            new() { Postcode = "TS16", Street = "Formby Walk", BinNumber = 1, FillLevel = 15, Weight = 4.5f, Density = 0.8f, Timestamp = now.AddMinutes(-60), Latitude = 54.5631, Longitude = -1.3123 },
            new() { Postcode = "TS16", Street = "Formby Walk", BinNumber = 1, FillLevel = 25, Weight = 6.2f, Density = 0.95f, Timestamp = now.AddMinutes(-50), Latitude = 54.5631, Longitude = -1.3123 },
            new() { Postcode = "TS16", Street = "Formby Walk", BinNumber = 1, FillLevel = 32, Weight = 7.1f, Density = 1.0f, Timestamp = now.AddMinutes(-40), Latitude = 54.5631, Longitude = -1.3123 },
            new() { Postcode = "TS16", Street = "Formby Walk", BinNumber = 1, FillLevel = 38, Weight = 7.8f, Density = 1.1f, Timestamp = now.AddMinutes(-30), Latitude = 54.5631, Longitude = -1.3123 },
            new() { Postcode = "TS16", Street = "Formby Walk", BinNumber = 1, FillLevel = 85, Weight = 16.2f, Density = 1.5f, Timestamp = now.AddMinutes(-20), Latitude = 54.5631, Longitude = -1.3123 }, // Spike
            new() { Postcode = "TS16", Street = "Formby Walk", BinNumber = 1, FillLevel = 88, Weight = 17.0f, Density = 1.52f, Timestamp = now.AddMinutes(-10), Latitude = 54.5631, Longitude = -1.3123 },

            // Bin 2 – Spike and drop
            new() { Postcode = "TS16", Street = "Alder Crescent", BinNumber = 2, FillLevel = 22, Weight = 5.2f, Density = 0.75f, Timestamp = now.AddMinutes(-50), Latitude = 54.5645, Longitude = -1.3105 },
            new() { Postcode = "TS16", Street = "Alder Crescent", BinNumber = 2, FillLevel = 28, Weight = 6.1f, Density = 0.8f, Timestamp = now.AddMinutes(-40), Latitude = 54.5645, Longitude = -1.3105 },
            new() { Postcode = "TS16", Street = "Alder Crescent", BinNumber = 2, FillLevel = 65, Weight = 12.4f, Density = 1.1f, Timestamp = now.AddMinutes(-30), Latitude = 54.5645, Longitude = -1.3105 }, // Spike
            new() { Postcode = "TS16", Street = "Alder Crescent", BinNumber = 2, FillLevel = 40, Weight = 9.1f, Density = 0.9f, Timestamp = now.AddMinutes(-20), Latitude = 54.5645, Longitude = -1.3105 }, // Drop
            new() { Postcode = "TS16", Street = "Alder Crescent", BinNumber = 2, FillLevel = 42, Weight = 9.4f, Density = 0.92f, Timestamp = now.AddMinutes(-10), Latitude = 54.5645, Longitude = -1.3105 },

            // Bin 3 – Consistent fill, no spike
            new() { Postcode = "TS17", Street = "Oakwood Drive", BinNumber = 3, FillLevel = 10, Weight = 3.8f, Density = 0.6f, Timestamp = now.AddMinutes(-55), Latitude = 54.5662, Longitude = -1.3150 },
            new() { Postcode = "TS17", Street = "Oakwood Drive", BinNumber = 3, FillLevel = 15, Weight = 4.2f, Density = 0.7f, Timestamp = now.AddMinutes(-45), Latitude = 54.5662, Longitude = -1.3150 },
            new() { Postcode = "TS17", Street = "Oakwood Drive", BinNumber = 3, FillLevel = 18, Weight = 5.0f, Density = 0.75f, Timestamp = now.AddMinutes(-35), Latitude = 54.5662, Longitude = -1.3150 },
            new() { Postcode = "TS17", Street = "Oakwood Drive", BinNumber = 3, FillLevel = 20, Weight = 5.8f, Density = 0.8f, Timestamp = now.AddMinutes(-25), Latitude = 54.5662, Longitude = -1.3150 },
            new() { Postcode = "TS17", Street = "Oakwood Drive", BinNumber = 3, FillLevel = 25, Weight = 6.4f, Density = 0.82f, Timestamp = now.AddMinutes(-15), Latitude = 54.5662, Longitude = -1.3150 }
        };

        context.SensorReadings.AddRange(bins);
        await context.SaveChangesAsync();
    }
}
