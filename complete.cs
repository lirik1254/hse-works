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
    [Activity(Label = "Цель", ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation, ScreenOrientation = ScreenOrientation.Locked)]
    public class complete : Activity
    {
        IList<string> stringsinput = new List<string>();
        IList<string> achievelist = new List<string>();
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.areReady);
            int count = Intent.GetIntExtra("index", -1);
            if (Intent.GetStringArrayListExtra("stringsinput") != null)
                stringsinput = Intent.GetStringArrayListExtra("stringsinput");
            if (Intent.GetStringArrayListExtra("achievelist") != null && Intent.GetStringArrayListExtra("achievelist").Count != 0)
                achievelist = Intent.GetStringArrayListExtra("achievelist");
            stringsinput = Intent.Extras.GetStringArrayList("stringsinput");
            TextView goaltext1 = FindViewById<TextView>(Resource.Id.GoalText1);
            TextView data = FindViewById<TextView>(Resource.Id.DateTextInput1);
            TextView difficult = FindViewById<TextView>(Resource.Id.DifficultTextInput1);
            Button continueButton = FindViewById<Button>(Resource.Id.buttonContinueGoal1);
            goaltext1.Text = stringsinput[count*4];
            data.Text = stringsinput[count * 4 + 1];
            difficult.Text = stringsinput[count * 4 + 3];
            Button delGoalButton = FindViewById<Button>(Resource.Id.DelGoalButton);
            continueButton.Click += (o, e) =>
            {
                var intent = new Intent(this, typeof(MainActivity));
                intent.PutStringArrayListExtra("stringsinput", stringsinput);
                intent.PutStringArrayListExtra("achievelist", achievelist);
                StartActivity(intent);
            };
            delGoalButton.Click += (o, e) =>
            {
                var intent = new Intent(this, typeof(MainActivity));
                for (int i = 0; i < 4; i++)
                    stringsinput.RemoveAt(count*4);
                Toast.MakeText(this, "Удаление произведено", ToastLength.Long);
                intent.PutStringArrayListExtra("stringsinput", stringsinput);
                intent.PutStringArrayListExtra("achievelist", achievelist);
                StartActivity(intent);
            };
            // Create your application here
        }
    }
}