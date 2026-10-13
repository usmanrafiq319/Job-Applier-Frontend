import {
  Component,
  input,
  output
} from '@angular/core';

import {
  RouterLink,
  RouterLinkActive
} from '@angular/router';


interface NavigationItem {

  label: string;

  icon: string;

  route: string;

  enabled: boolean;

}


@Component({
  selector: 'app-sidebar',

  imports: [
    RouterLink,
    RouterLinkActive
  ],

  templateUrl: './sidebar.html',

  styleUrl: './sidebar.css'
})
export class Sidebar {

  readonly showCloseButton =
    input(false);


  readonly closeRequested =
    output<void>();


  protected readonly navigationItems:
    NavigationItem[] = [

    {
      label: 'Dashboard',
      icon: '⌂',
      route: '/dashboard',
      enabled: true
    },

    {
      label: 'Analyze Job',
      icon: '⌕',
      route: '/jobs/analyze',
      enabled: true
    },

    {
      label: 'Jobs',
      icon: '▣',
      route: '/jobs',
      enabled: true
    },

    {
      label: 'Outreach',
      icon: '✉',
      route: '/outreach',
      enabled: true
    },

    {
      label: 'Applications',
      icon: '✓',
      route: '/applications',
      enabled: true
    },

    {
      label: 'Profile',
      icon: '◉',
      route: '/profile',
      enabled: true
    }

  ];


  protected close(): void {

    this.closeRequested.emit();

  }

}