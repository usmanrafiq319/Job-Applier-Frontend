
import {Component,signal} from '@angular/core';
import { RouterOutlet} from '@angular/router';
import {Sidebar} from '../sidebar/sidebar';
import {Topbar} from '../topbar/topbar';


@Component({

  selector: 'app-shell',

  imports: [
    RouterOutlet,
    Sidebar,
    Topbar
  ],

  templateUrl: './app-shell.html',

  styleUrl: './app-shell.css'

})
export class AppShell {

  protected readonly mobileSidebarOpen =
    signal(false);


  protected openSidebar(): void {

    this.mobileSidebarOpen.set(true);

  }


  protected closeSidebar(): void {

    this.mobileSidebarOpen.set(false);

  }

}