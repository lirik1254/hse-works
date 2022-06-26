using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Android.Content.PM;
using AndroidX.AppCompat.App;
using Android.Widget;


namespace ProjectCurs
{
    [Activity(Label = "Создание цели", ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation, ScreenOrientation = ScreenOrientation.Locked)]
    public class OneGoalActivity : AppCompatActivity
    {
        static public IList<string> achievelist = new List<string>();
        [Obsolete]
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            // Create your application here
            SetContentView(Resource.Layout.oneGoal_activity);
            IList<string> stringsinput = new List<string>();
            if (Intent.GetStringArrayListExtra("stringsinput") != null)
                stringsinput = Intent.GetStringArrayListExtra("stringsinput");
            if (Intent.GetStringArrayListExtra("achievelist") != null && Intent.GetStringArrayListExtra("achievelist").Count != 0)
                achievelist = Intent.GetStringArrayListExtra("achievelist");
            EditText DataInput = FindViewById<EditText>(Resource.Id.dataEditText1);
            ImageButton CalendarButton = FindViewById<ImageButton>(Resource.Id.CalendarButton);
            CalendarButton.Click += DateSelect_OnClick;
            Button continueButton = FindViewById<Button>(Resource.Id.buttonContinue);
            EditText pointInputText = FindViewById<EditText>(Resource.Id.pointInputText);
            EditText goalInputText = FindViewById<EditText>(Resource.Id.goalEditText);
            continueButton.Click += (sender, e) =>
            {
                if (goalInputText.Text.Length == 0)
                {
                    Toast.MakeText(this, "Пропущен ввод цели", ToastLength.Long).Show();
                }
                else if (DataInput.Text.Length == 0)
                {
                    Toast.MakeText(this, "Пропущен ввод даты", ToastLength.Long).Show();
                }
                else if (inputData(DataInput.Text) == false)
                {
                    Toast.MakeText(this, "Некорректный ввод даты", ToastLength.Long).Show();
                }
                else if (pointInputText.Text.Length == 0)
                {
                    Toast.MakeText(this, "Пропущен ввод сложности цели", ToastLength.Long).Show();
                }
                else if (int.Parse(pointInputText.Text) < 1 || int.Parse(pointInputText.Text) > 10)
                {
                    Toast.MakeText(this, "Сложность цели - число от 1 до 10", ToastLength.Long).Show();
                }
                else
                {
                    var intent = new Intent(this, typeof(Goal));
                    string Data = DataInput.Text;
                    string Point = pointInputText.Text;
                    string Goal = goalInputText.Text;
                    intent.PutExtra("Data", Data);
                    intent.PutExtra("Point", Point);
                    intent.PutExtra("Goal", Goal);
                    intent.PutStringArrayListExtra("stringsinput", stringsinput);
                    intent.PutStringArrayListExtra("achievelist", achievelist);
                    StartActivity(intent);
                }
            };
        }

        [Obsolete]
        void DateSelect_OnClick(object sender, EventArgs eventArgs)
        {
            EditText DataInput = FindViewById<EditText>(Resource.Id.dataEditText1);
            DatePickerFragment frag = DatePickerFragment.NewInstance(delegate (DateTime time)
            {
                DataInput.Text = time.ToShortDateString();
            });
            frag.Show(FragmentManager, DatePickerFragment.TAG);
        }
        static public bool inputData(string data)
        {
            int x;
            if (data.Length != 10)
                return false;
            if (data[2].ToString() != "." || data[5].ToString() != "." || int.TryParse(data.Substring(0, 2).ToString(), out x) == false ||
                int.TryParse(data.Substring(3, 2).ToString(), out x) == false || int.TryParse(data.Substring(6, 4).ToString(), out x) == false)
                return false;
            DateTime current = DateTime.Now;
            int day = int.Parse(data.Substring(0, 2));
            int month = int.Parse(data.Substring(3, 2));
            int year = int.Parse(data.Substring(6, 4));
            if (year < current.Year || month < current.Month)
                return false;
            else if (day < current.Day && (year > current.Year || month > current.Month))
                return true;
            try
            {
                DateTime temp = new DateTime(year, month, day);
            }
            catch (System.ArgumentOutOfRangeException)
            {
                return false;
            }
            return true;
        }
    }
}