using Android.App;
using Android.Content;
using Android.Content.PM;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ProjectCurs
{
    [Activity(Label = "Достижения", ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation, ScreenOrientation = ScreenOrientation.Locked)]
    public class achievements : Activity
    {
        IList<string> achievelist = new List<string>() { "false", "" };
        IList<string> stringsinput = new List<string>();
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.Achievements);
            if (Intent.GetStringArrayListExtra("stringsinput") != null)
                stringsinput = Intent.Extras.GetStringArrayList("stringsinput");
            if (Intent.GetStringArrayListExtra("achievelist") != null && Intent.GetStringArrayListExtra("achievelist").Count != 0)
                achievelist = Intent.Extras.GetStringArrayList("achievelist");
            TextView points = FindViewById<TextView>(Resource.Id.howMuchPoints);
            TextView first = FindViewById<TextView>(Resource.Id.first);
            TextView second = FindViewById<TextView>(Resource.Id.second);
            TextView fivepoints = FindViewById<TextView>(Resource.Id.fivepoints);
            TextView fiftypoints = FindViewById<TextView>(Resource.Id.fiftypoints);
            TextView twohundredpoints = FindViewById<TextView>(Resource.Id.twohundredpoints);
            TextView onethousandpoints = FindViewById<TextView>(Resource.Id.onethousandpoints);
            if (achievelist[1] == "")
                points.Text = "0";
            else
                points.Text = achievelist[1];
            if (achievelist[0] == "true")
                first.SetBackgroundColor(Android.Graphics.Color.DarkGreen);
            if (achievelist[1] != "")
            {
                points.Text = achievelist[1];
                second.SetBackgroundColor(Android.Graphics.Color.DarkGreen);
                if (int.Parse(achievelist[1]) >= 5)
                    fivepoints.SetBackgroundColor(Android.Graphics.Color.DarkGreen);
                if (int.Parse(achievelist[1]) >= 50)
                    fiftypoints.SetBackgroundColor(Android.Graphics.Color.DarkGreen);
                if (int.Parse(achievelist[1]) >= 200)
                    twohundredpoints.SetBackgroundColor(Android.Graphics.Color.DarkGreen);
                if (int.Parse(achievelist[1]) >= 1000)
                    onethousandpoints.SetBackgroundColor(Android.Graphics.Color.DarkGreen);
            }
                Button continuegoal = FindViewById<Button>(Resource.Id.buttonContinueGoal2);
            continuegoal.Click += (o, e) =>
            {
                var intent = new Intent(this, typeof(MainActivity));
                intent.PutStringArrayListExtra("stringsinput", stringsinput);
                intent.PutStringArrayListExtra("achievelist", achievelist);
                StartActivity(intent);
            };
            // Create your application here
        }
    }
}