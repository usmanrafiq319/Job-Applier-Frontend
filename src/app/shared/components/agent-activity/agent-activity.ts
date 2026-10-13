import {
  Component,
  computed,
  input
} from '@angular/core';

import {
  AgentRun,
  AgentStep
} from '../../../models/agent.model';


interface ActivityStep {

  step: AgentStep;

  title: string;

  description: string;

}


@Component({
  selector: 'app-agent-activity',

  imports: [],

  templateUrl:
    './agent-activity.html',

  styleUrl:
    './agent-activity.css'
})
export class AgentActivity {

  readonly run =
    input.required<AgentRun>();


  protected readonly steps:
    ActivityStep[] = [

    {
      step:
        'LOAD_PROFILE',

      title:
        'Load Profile',

      description:
        'Load career profile and resume context.'
    },

    {
      step:
        'PARSE_JOB',

      title:
        'Parse Job',

      description:
        'Extract information from the vacancy.'
    },

    {
      step:
        'ANALYZE_REQUIREMENTS',

      title:
        'Analyze Requirements',

      description:
        'Identify skills and role requirements.'
    },

    {
      step:
        'MATCH_PROFILE',

      title:
        'Match Profile',

      description:
        'Compare job requirements with your profile.'
    },

    {
      step:
        'RETRIEVE_EXPERIENCE',

      title:
        'Retrieve Experience',

      description:
        'Retrieve relevant projects and experience using RAG.'
    },

    {
      step:
        'CALCULATE_SCORE',

      title:
        'Calculate Score',

      description:
        'Calculate the final opportunity match score.'
    },

    {
      step:
        'GENERATE_EMAIL',

      title:
        'Generate Outreach',

      description:
        'Generate personalized outreach.'
    },

    {
      step:
        'WAIT_FOR_APPROVAL',

      title:
        'Human Approval',

      description:
        'Wait for user approval before external action.'
    },

    {
      step:
        'CREATE_GMAIL_DRAFT',

      title:
        'Create Gmail Draft',

      description:
        'Create the approved Gmail draft.'
    },

    {
      step:
        'SAVE_APPLICATION',

      title:
        'Save Application',

      description:
        'Store the application tracking record.'
    }

  ];


  private readonly currentIndex =
    computed(() => {

      const current =
        this.run().currentStep;


      if (!current) {
        return -1;
      }


      return this.steps
        .findIndex(
          item =>
            item.step === current
        );

    });


  protected stepState(
    index: number
  ):
    'completed' |
    'active' |
    'pending' {

    const current =
      this.currentIndex();


    if (index < current) {
      return 'completed';
    }


    if (index === current) {
      return 'active';
    }


    return 'pending';

  }

}