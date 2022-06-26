using System;
using Android.App;
using Android.OS;
using Android.Runtime;
using Android.Views;
using AndroidX.AppCompat.Widget;
using AndroidX.AppCompat.App;
using Google.Android.Material.FloatingActionButton;
using Google.Android.Material.Snackbar;
using Android.Content;
using Android.Widget;
using Android.Content.PM;
using System.Collections.Generic;
using Android.Graphics;

namespace ProjectCurs
{
    [Activity(Label = "@string/app_name", Theme = "@style/AppTheme", MainLauncher = true, ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation, ScreenOrientation = ScreenOrientation.Locked)]
    public class MainActivity : AppCompatActivity
    {
        protected override void OnCreate(Bundle savedInstanceState) 
        {
            List<Button> buttons = new List<Button>();
            IList<string> stringsinput = new List<string>();
            IList<string> achievelist = new List<string>() { "false", ""};
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.activity_main);
            if (Intent.GetStringArrayListExtra("stringsinput") != null)
                stringsinput = Intent.Extras.GetStringArrayList("stringsinput");
            if (Intent.GetStringArrayListExtra("achievelist") != null && Intent.GetStringArrayListExtra("achievelist").Count != 0)
                achievelist = Intent.Extras.GetStringArrayList("achievelist");
            if (stringsinput.Count != 0)
                achievelist[0] = "true";
            Button oneGoalButton = FindViewById<Button>(Resource.Id.OneGoalButton);
            oneGoalButton.Click += (sender, e) =>
            {
                var intent = new Intent(this, typeof(OneGoalActivity));
                intent.PutStringArrayListExtra("stringsinput", stringsinput);
                StartActivity(intent);
            };
            Button statistics = FindViewById<Button>(Resource.Id.buttonStatictics);
            if (stringsinput.Count == 0)
            {
                statistics.Click += (sender, e) =>
                {
                    Toast.MakeText(this, "Вы не создали ещё ни одной цели", ToastLength.Long).Show();
                };
            }
            else
            {
                statistics.Click += (sender, e) =>
                {
                    var intent = new Intent(this, typeof(statistics));
                    intent.PutStringArrayListExtra("stringsinput", stringsinput);
                    intent.PutStringArrayListExtra("achievelist", achievelist);
                    StartActivity(intent);
                };
            }
            Button achievement = FindViewById<Button>(Resource.Id.button3);
            achievement.Click += (sender, e) =>
            {
                var intent = new Intent(this, typeof(achievements));
                intent.PutStringArrayListExtra("stringsinput", stringsinput);
                intent.PutStringArrayListExtra("achievelist", achievelist);
                StartActivity(intent);
            };
            float firstCoefY = 972f;
            float firstCoefX = 60f;
            float coefY = 412.5f;
            float coefX = 491.875f + 32;
            int Height = 323;
            int Width = 450;
            RelativeLayout layout = FindViewById<RelativeLayout>(Resource.Id.mainPage);
            int x = 1772;
            layout.SetMinimumHeight(x);
            Button sm1 = new Button(this);
            //ImageView s1 = new ImageView(this);
            //s1.SetImageResource(Resource.Drawable.Calendar);
            //s1.SetMaxHeight(20);
            //s1.SetMaxHeight(20);
            //s1.SetX(-100);
            //s1.SetY(-700);
            //s1.SetZ(10);
            //layout.AddView(s1);
            if (stringsinput != null)
                for (int i = 0; i < stringsinput.Count / 4; i++)
                {
                    sm1 = new Button(this.ApplicationContext);
                    if (i == 0)
                    {
                        sm1.Text = stringsinput[0];
                        sm1.SetAllCaps(false);
                        if (int.Parse(stringsinput[i * 4 + 2]) <= 0)
                        {
                            stringsinput[i * 4 + 2] = 0.ToString();
                            sm1.SetBackgroundColor(Color.MediumSpringGreen);
                        }
                        else
                            sm1.SetBackgroundColor(Color.LightGoldenrodYellow);
                        sm1.SetTextColor(Color.Black);
                        sm1.SetX(firstCoefX + coefX);
                        sm1.SetY(firstCoefY - coefY);
                        sm1.SetHeight(320);
                        sm1.SetWidth(450);
                        buttons.Add(sm1);
                        layout.AddView(sm1);
                    }
                    if (i % 2 == 0 && i != 0)
                    {
                        sm1.Text = stringsinput[i*4];
                        sm1.SetAllCaps(false);
                        if (int.Parse(stringsinput[i * 4 + 2]) <= 0)
                        {
                            stringsinput[i * 4 + 2] = 0.ToString();
                            sm1.SetBackgroundColor(Color.MediumSpringGreen);
                        }
                        else
                            sm1.SetBackgroundColor(Color.LightGoldenrodYellow);
                        sm1.SetTextColor(Color.Black);
                        sm1.SetX(firstCoefX + coefX);
                        sm1.SetY(firstCoefY);
                        sm1.SetHeight(Height);
                        sm1.SetWidth(Width);
                        buttons.Add(sm1);
                        layout.AddView(sm1);
                    }
                    if (i % 2 == 1)
                    {
                        if (i != 3 && i != 1)
                        {
                            x += 420;
                            layout.SetMinimumHeight(x);
                        }
                        if (i != 1)
                            firstCoefY += coefY;
                        sm1.Text = stringsinput[i*4];
                        sm1.SetAllCaps(false);
                        if (int.Parse(stringsinput[i * 4 + 2]) <= 0)
                        {
                            stringsinput[i * 4 + 2] = 0.ToString();
                            sm1.SetBackgroundColor(Color.MediumSpringGreen);
                        }
                        else
                            sm1.SetBackgroundColor(Color.LightGoldenrodYellow);
                        sm1.SetTextColor(Color.Black);
                        sm1.SetX(firstCoefX);
                        sm1.SetY(firstCoefY);
                        sm1.SetHeight(320);
                        sm1.SetWidth(450);
                        buttons.Add(sm1);
                        layout.AddView(sm1);
                    }
                }
            int count = -1;
            foreach(Button b in buttons)
            {
                b.Click += (sender, e) =>
                {
                    var intent = new Intent(this, typeof(Goal));
                    count = buttons.IndexOf(b);
                    if (int.Parse(stringsinput[count * 4 + 2]) <= 0)
                    {
                        var intent1 = new Intent(this, typeof(complete));
                        intent1.PutStringArrayListExtra("stringsinput", stringsinput);
                        intent1.PutStringArrayListExtra("achievelist", achievelist);
                        intent1.PutExtra("index", count);
                        StartActivity(intent1);
                    }
                    else
                    {
                        intent.PutExtra("fromMain", "yes");
                        intent.PutStringArrayListExtra("stringsinput", stringsinput);
                        intent.PutStringArrayListExtra("achievelist", achievelist);
                        intent.PutExtra("index", count);
                        StartActivity(intent);
                    }
                };
            }
            
        }
    }
}
