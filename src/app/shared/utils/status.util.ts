import {
  BadgeTone
} from '../components/status-badge/status-badge';


export function formatStatus(status: string): string {

  return status
    .replaceAll('_', ' ')
    .toLowerCase()
    .replace(
      /\b\w/g,
      character =>
        character.toUpperCase()
    );

}


export function getStatusTone( status: string): BadgeTone {

  switch (status) {

    /* Positive */

    case 'HIGH_MATCH':
    case 'REPLIED':
    case 'INTERVIEW':
    case 'OFFER':
    case 'APPROVED':
    case 'CREATED_IN_GMAIL':
    case 'COMPLETED':

      return 'success';


    /* Work in progress */

    case 'ANALYZED':
    case 'SENT':
    case 'SAVED':
    case 'GENERATED':
    case 'RUNNING':

      return 'info';


    /* Waiting */

    case 'READY':
    case 'DRAFT':
    case 'EDITED':
    case 'PENDING':
    case 'WAITING_FOR_APPROVAL':

      return 'warning';


    /* Negative */

    case 'LOW_MATCH':
    case 'REJECTED':
    case 'FAILED':
    case 'CANCELLED':

      return 'danger';


    default:

      return 'neutral';

  }

}