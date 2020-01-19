package com.example.emotionapp;

import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;
import android.widget.ListView;
import android.widget.ArrayAdapter;

import java.util.ArrayList;

public class ScrollingActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scrolling);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        // show the name and other information for the user
        String name = "John Doe";
        int age = 15;

        TextView name_text= (TextView) findViewById(R.id.name);
        TextView age_text  =(TextView) findViewById(R.id.age);

        name_text.setText("Name : " + name);
        age_text.setText("Age : " + String.valueOf(age));

        // fill the list of feedback given - needs to be connected to the database
        String[] test_array = {"test 1", "test_2", "test_3"};
        fillFeeedbackList(test_array);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_scrolling, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    public void fillFeeedbackList(String[] feedback_ques) {
        ListView listview = (ListView) findViewById(R.id.feedback_list);

        ArrayAdapter adapter = new ArrayAdapter(this, android.R.layout.simple_list_item_1, feedback_ques);
        listview.setAdapter(adapter);
    }
}
